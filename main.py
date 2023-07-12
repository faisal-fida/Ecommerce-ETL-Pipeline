import time
import sys
import random
import aiohttp
import asyncio
import datetime
from flask import Flask
import json as Json
import pandas as pd
from loguru import logger
import copy
from handle_database.firesore import upload_data, retrieve_data, delete_data
from data_processing.data_cleaning import clean_data
from data_processing.initial import data_headers_payloads
from scraping_list_product_modules import *
from handle_database.storage_connector import CloudStorageConnector
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

URL = "https://www.thredup.com/api/v1/shop/graphql"

payload_products = data_headers_payloads[0]
headers_products = data_headers_payloads[1]

with open("data_processing/proxies.txt") as f:
    proxies = f.read().split("\n")
    
# function to make async requests to the product url and create_task of the requests and return the task
async def get_product(session, itemNumber):
    payload_products_execute = copy.deepcopy(payload_products)
    payload_products_execute['variables']['itemNumber'] = int(itemNumber)
    proxy = proxies[random.randint(0, len(proxies) - 1)]
    try:
        if proxy == "localhost":
            task = asyncio.create_task(session.post(URL, json=payload_products_execute, headers=headers_products))
            return task
        
        task = asyncio.create_task(session.post(URL, json=payload_products_execute, headers=headers_products, proxy=proxy))
        return task
    except:
        print("Error occur when using proxies")
        task = asyncio.create_task(session.post(URL, json=payload_products_execute, headers=headers_products))
        return task
    
# function to add the products itemnumbers in the itemnumbersupdateList to keep db of 10K products
def add_products_instock(OutStock_Counter):
    with open('data_processing/itemnumbersupdate.txt', 'r+') as re:
        lines = re.read().splitlines()
        lines_to_remove = lines[:OutStock_Counter]
        lines_to_add = lines[OutStock_Counter:]

        with open('data_processing/itemnumbersupdate.txt', 'r+') as re:
            for line in lines_to_add:
                if line not in lines_to_remove:
                    re.write(line + '\n')
    return lines_to_remove

    for i in range(OutStock_Counter):
        with open('data_processing/itemnumbersupdate.txt') as re:
            itemnumbersupdateList = [line.strip() for line in re]

# handle the retry for thredup api callss
async def handle_retry(retry_after):
    if retry_after is not None:
        try:
            print(f"Sleeping for {retry_after}")
            await asyncio.sleep(int(retry_after) + 3)
            #time.sleep(int(retry_after) + 3)
        except ValueError:
            logger.error("Handle Retry error 1.")
            try:
                timestamp = datetime.datetime.strptime(retry_after, "%a, %d %b %Y %H:%M:%S %Z")
                sleep_time = (timestamp - datetime.datetime.now(datetime.timezone.utc)).total_seconds()
                #time.sleep(int(sleep_time) + 3)
                await asyncio.sleep(int(sleep_time) + 3)
            except ValueError:
                logger.error("Handle Retry error 2.")
                pass
    else:
        time.sleep(70)

async def handle_response(response, data_products, OutStock_Counter, prev_retry_after, i, itemNumber, want_delete=False):
    '''
    Response Successfull: Get products json and add to data_products list.
    Response Unsuccessfull: Get retry_after time from server, wait for that time and try again.
    '''
    try:
        if response.status == 200:
            response_data = await response.read()
            data_product = Json.loads(response_data)['data']['itemByItemNumber']
            if not data_product:
                print(itemNumber, "No data for this item")
                return
            
            if data_product['availability'] == 'InStock':
                data_products.append(data_product)
            else:
                print(itemNumber, "This item is outstock")
                OutStock_Counter += 1
                
                if want_delete == True:
                    delete_data(db, f'thredup_{data_product["itemNumber"]}')
                
        elif response.status == 429:
            retry_after = response.headers.get("Retry-After") # 429
            if retry_after != prev_retry_after:
                print(f"Got Error 429 | Scraped: {i} | OutStockProducts: {OutStock_Counter} | Sleeping for {retry_after}")
                logger.debug(f"Retry-After changed from {prev_retry_after} to {retry_after}")
                prev_retry_after = retry_after
                await handle_retry(retry_after)
            await response.release()
        else:
            print(f"Unexpected status code {response.status}")
            logger.error(f"Unexpected status code {response.status}")
            await response.release()
    except Exception as e:
        
        print(itemNumber, f"Releasing Response: {e}", i)
        logger.error(f"{itemNumber}: Releasing Response: {e}", i)


async def get_products(itemNumbersList, want_delete=False):
    '''
    Create a session, make requests for all the itemNumbers, create tasks and execute every 5.
    Gether responses and send to handle_repsonse function for further processing.
    At the end return data_products (Json of all products scraped).
    '''
    OutStock_Counter, prev_retry_after, data_products = 0, None, []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, itemNumber in enumerate(itemNumbersList):
            try:
                task = get_product(session, itemNumber)
                tasks.append(task)
            except Exception as e:
                print("Error when calling request", e)
                time.sleep(5)
                
            if i % 5 == 0:
                responses = await asyncio.gather(*tasks)
                logger.info(f"Responses: {len(responses)}")
                tasks = []
                retry_after = None
                for response_task in responses:
                    try:
                        response = await response_task
                        await handle_response(response, data_products, OutStock_Counter, prev_retry_after, i, itemNumber, want_delete)
                    except Exception as e:
                        time.sleep(2)
                        print("Error when handling response", e)
                        
                
        if tasks:
            responses = await asyncio.gather(*tasks)
            logger.info(f"Responses: {len(responses)}")
            tasks = []
            for response_task in responses:
                try:
                    response = await response_task
                    await handle_response(response, data_products, OutStock_Counter, prev_retry_after, i, itemNumber, want_delete)
                except Exception as e:
                    time.sleep(2)
                    print("Error when handling response", e)
    return data_products

def parse_products(data_products):
    '''
    Get Json from get_products function and converitng it into Dataframe.
    Merging Dataframes into one.
    Output the file df_products.csv (as a backup) so that it can be read by clean_data function for further processing.
    '''
    df_products = pd.DataFrame()
    for data_product in data_products:
        try:
            df_product = pd.DataFrame.from_dict(data_product, orient='index').transpose()
            df_products = pd.concat([df_products, df_product], ignore_index=True)
        except TypeError:
            logger.error(f"Product {data_product} has no len.")
            pass
    
    return df_products

def generate_df_final(df, df_new):
    # Get ids in df_new but not in df
    new_ids = set(df_new['itemNumber']).difference(df['itemNumber'])

    # Get rows in df_new with new ids
    new_rows = df_new[df_new['itemNumber'].isin(new_ids)]

    # Get rows in df where the id is also in df_new, but the price is different
    diff_rows = pd.merge(df, df_new, on='itemNumber', how='inner', suffixes=('_old', '_new'))
    diff_rows = diff_rows[diff_rows['price_old'] != diff_rows['price_new']]
    print(len(new_rows), len(diff_rows))
    # Concatenate new_rows and diff_rows into df_final
    df_final = pd.concat([new_rows, diff_rows])
    df_final = df_final.drop_duplicates(subset="itemNumber")
    
    # Select rows contains in current df but not contains in new df
    df_diff = df[~df.itemNumber.isin(df_new.itemNumber)]
    return df_final.reset_index(), df_diff.reset_index()

async def main():
    data_initial_products = get_initial_products(json_amount=250, max_page=201)
    df_initial_products = parse_initial_products(data_initial_products) 
    
    cloud_storage_connector.insertToStorage(df_initial_products.to_dict("records"), "thredup/women_jeans", "new_products.json")
    df_initial_products.to_csv("output/new_products.csv", index=False)
    df_current_products = pd.DataFrame(retrieve_data(db))
    df_current_products = df_current_products[['ItemID', 'Price']]
    df_current_products.columns = ["itemNumber", "price"]
    df_final, df_diff = generate_df_final(df_current_products, df_initial_products)
    
    # df_final = df_initial_products
    print("Len df_final", len(df_final))
    print("Len df_diff", len(df_diff))
    
    # Counting Time
    start_time = time.perf_counter()
    # Scraping Products
    data_products = await get_products(df_final["itemNumber"].to_list())
    end_time = time.perf_counter()
    print(f"Time taken to Scrape {len(data_products)} products: {end_time - start_time} | Now parsing products..")
    # Parsing Products (JSON to DF)
    df_products = parse_products(data_products)
    
    # Cleaning the DataFrame and Getting Json back
    dataJson = clean_data(df_products)
    # If got Json back than uploading to Database (Firestore)
    if dataJson is not None:
        upload_data(db, dataJson)

    print("Starting to check and remove OutStock in existing database")
    await get_products(df_diff["itemNumber"].to_list(), want_delete=True)


firebase_admin.initialize_app()
db = firestore.client()
cloud_storage_connector = CloudStorageConnector()

app = Flask(__name__)
@app.route("/", methods=["POST"])
def index():
    asyncio.run(main())
    
    return ("", 204)
    

# if __name__ == '__main__':
#     PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

#     # This is used when running locally. Gunicorn is used to run the
#     # application on Cloud Rufn. See entrypoint in Dockerfile.
#     app.run(host="127.0.0.1", port=PORT, debug=True)