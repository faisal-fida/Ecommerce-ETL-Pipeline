import time
import requests
import json as Json
import pandas as pd
import random
from data_processing.data_cleaning import clean_data
from data_processing.agolio_upload import db_upload
from data_processing.initial import data_headers_payloads

URL = "https://www.thredup.com/api/v1/shop/graphql"

payload_initial_products = data_headers_payloads[0]
headers_initial_products = data_headers_payloads[1]
payload_final_products = data_headers_payloads[2]
headers_final_products = data_headers_payloads[3]


def post_request(URL, payload, headers):
    return requests.request("POST", URL, json=payload, headers=headers).json()


def json_variables(itemNumber=137186287, json_amount=119, type_products='final', json_page=2, json_visitorId=33, json_parentId=74, json_queryId=746):
    if type_products == 'initial':
        payload_initial_products['variables']['amount'] = json_amount
        payload_initial_products['variables']['page'] = json_page
        # payload_initial_products['variables']['visitorId'] = json_visitorId
        # payload_initial_products['variables']['bucketingKey'] = json_visitorId
        # payload_initial_products['variables']['parentId'] = json_parentId
        # payload_initial_products['variables']['queryId'] = json_queryId
        # headers_initial_products['auth-token'] = auth_token
        # headers_initial_products['cookie'] = cookie
    else:
        payload_final_products['variables']['itemNumber'] = itemNumber
        # payload_final_products['variables']['visitorId'] = json_visitorId
        # payload_final_products['variables']['queryId'] = json_queryId
        # payload_final_products['variables']['resultId'] = json_resultId
        # headers_final_products['auth-token'] = auth_token
        # headers_final_products['cookie'] = cookie


def get_initial_products():
    data_initial_products = []
    # start_time = time.time()

    for idx in range(1, 2):
        print(f'Scraping Initial Products Page: {idx}', end='\r')
        json_variables(type_products='initial', json_page=idx)
        try:
            data_initial_product = post_request(
                URL, payload_initial_products, headers_initial_products)['data']['items']['nodes']
            data_initial_products.append(data_initial_product)
        except Exception as e:
            print(f"\nError retrieving data_initial_product: {e} \n")
            pass
        time.sleep(20)

    # end_time = time.time()
    # print(f"Time taken to Scrape {idx} Pages: {end_time - start_time}")

    return data_initial_products


def get_final_products(itemNumbersList):
    data_final_products = []
    start_time = time.time()

    for idx, itemNumber in enumerate(itemNumbersList[:], 1):
        print(f'Scraping Final Product No: {idx} {itemNumber}', end='\r')
        json_variables(itemNumber)
        try:
            data_final_product = post_request(
                URL, payload_final_products, headers_final_products)['data']
            data_final_products.append(data_final_product)
            itemNumbersList.remove(itemNumber)
            if idx == 10:
                break
        except Exception as e:
            print(f"\nError retrieving data_final_product: {e} \n")
            pass
        time.sleep(random.uniform(1, 2))

    end_time = time.time()
    print(f"Time taken to Scrape {idx} Products: {end_time - start_time}")

    return data_final_products


def parse_products(data_products, type_products='final'):
    df_products = pd.DataFrame()

    if type_products == 'final':
        for data_product in data_products:
            df_product = pd.DataFrame.from_dict(
                data_product['itemByItemNumber'], orient='index')
            df_product = df_product.transpose()
            df_products = pd.concat(
                [df_products, df_product], ignore_index=True)
        return df_products

    else:
        for data_product in data_products:
            df_product = pd.DataFrame(data_product)
            df_products = pd.concat(
                [df_products, df_product], ignore_index=True)
        return df_products['itemNumber'].to_list()


def main():
    data_initial_products = get_initial_products()
    itemNumbersList = parse_products(
        data_initial_products, type_products='initial')

    data_final_products = get_final_products(itemNumbersList)
    df_final_products = parse_products(data_final_products)

    return df_final_products


if __name__ == '__main__':
    # df_final_products = main()
    # df_final_products.to_csv('output/df_final_products.csv')
    dataJson = clean_data()
    db_upload(dataJson)
