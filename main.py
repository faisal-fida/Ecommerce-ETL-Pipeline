import time
import requests
import json as Json
import pandas as pd
import random
from data_processing.data_cleaning import clean_data
from data_processing.agolio_upload import db_upload
from data_processing.initial import data_headers_payloads

URL = "https://www.thredup.com/api/v1/shop/graphql"

payload_products = data_headers_payloads[0]
headers_products = data_headers_payloads[1]

with open('data_processing/itemnumbers.txt', 'r') as re:
    itemNumbersList = re.read().splitlines()


def post_request(URL, payload, headers):
    return requests.request("POST", URL, json=payload, headers=headers).json()


def json_variables(itemNumber=137186287):
    payload_products['variables']['itemNumber'] = itemNumber
    # payload_products['variables']['visitorId'] = json_visitorId
    # payload_products['variables']['queryId'] = json_queryId
    # payload_products['variables']['resultId'] = json_resultId
    # headers_products['auth-token'] = auth_token
    # headers_products['cookie'] = cookie


def get_products(itemNumbersList):
    data_products = []
    start_time = time.time()

    for idx, itemNumber in enumerate(itemNumbersList[:], 1):
        print(f'Scraping Final Product No: {idx} {itemNumber}', end='\r')
        json_variables(itemNumber)
        try:
            data_product = post_request(URL, payload_products, headers_products)['data']
            data_products.append(data_product)
            itemNumbersList.remove(itemNumber)
            # if idx == 10:
            #     break
        except Exception as e:
            print(f"\nError retrieving data_product: {e} \n")
            pass
        time.sleep(random.uniform(1, 2))

    end_time = time.time()
    print(f"Time taken to Scrape {idx} Products: {end_time - start_time}")

    return data_products


def parse_products(data_products):
    df_products = pd.DataFrame()

    for data_product in data_products:
        df_product = pd.DataFrame.from_dict(data_product['itemByItemNumber'], orient='index')
        df_product = df_product.transpose()
        df_products = pd.concat([df_products, df_product], ignore_index=True)
        df_products.to_csv('output/df_products.csv')


def main():
    data_products = get_products(itemNumbersList)
    df_products = parse_products(data_products)


if __name__ == '__main__':
    df_products = main()
    dataJson = clean_data()
    #db_upload(dataJson)