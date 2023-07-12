import time
import requests
import json as Json
import pandas as pd

URL = "https://www.thredup.com/api/v1/shop/graphql"

payload_initial_products = {
    'operationName': 'getItems',
    'variables': {
        'amount': 1000,
        'context': 'plp',
        'filters': {
            'department_tags': [
                'women',
            ],
            'category_tags': [
                'jeans',
            ],
        },
        'itemQueryContext': {
            'clientModule': 'core_other',
            'clientPageType': 'shop-listings',
        },
        'page': 1,
        'query': '',
        "sortBy": "newest_first",
        'target': None,
        'userInfo': {
            'bucketingKey': '3320415043',
            'hasPurchasedOrder': False,
            'isInternational': True,
            'mdcOverride': False,
            'userId': None,
            'userWarehouseIds': [
                16,
                5,
            ],
            'visitorId': '3320415043',
        },
        'excludes': {
            'warehouse_id': [
                20,
            ],
        },
    },
    'extensions': {
        'persistedQuery': {
            'version': 1,
            'sha256Hash': 'd497d7f56926c26b91a852bf092559cf1b1081812eeb10205947be4a57a9826c',
        },
    },
}


cookies = {
    'tup_jwt_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ2aXNpdG9yX2lkIjozMzQ3MTAzODMwfQ.ukau1AkFXXLG8Ji_LMoPtFxt21Cg9AGgzVsu-A_lit6_zQj0Yx0y0dozO8Huhc0l-ONXfF0mhS5nnGZuR1cU9gN0TQs5pZz50_zktYOsibBkDFq8KMdwUizl0sIdusQLWfmJ_q34e_XmPM4lstyfcvjdGYFKiR4HAmxvfc3NsgrRhA3KSyIQ8fZzsh1UpLoCgcg6UQxK4Y4Ds3ADQ_pd5N3zlVbuIQJ4TEU8J3LirtW9bOXM8c_ObLiRfKgmWbacvva16jFLIXfv5CM0S2VA7Rhu90sdWbl7sljqu9lfbt9jklazQwOwwekL-_bg3tbXgeFAMY1stoD7fkJIVoP39w'
}

headers = {
    'authority': 'www.thredup.com',
    'auth-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ2aXNpdG9yX2lkIjozMzQ3MTAzODMwfQ.ukau1AkFXXLG8Ji_LMoPtFxt21Cg9AGgzVsu-A_lit6_zQj0Yx0y0dozO8Huhc0l-ONXfF0mhS5nnGZuR1cU9gN0TQs5pZz50_zktYOsibBkDFq8KMdwUizl0sIdusQLWfmJ_q34e_XmPM4lstyfcvjdGYFKiR4HAmxvfc3NsgrRhA3KSyIQ8fZzsh1UpLoCgcg6UQxK4Y4Ds3ADQ_pd5N3zlVbuIQJ4TEU8J3LirtW9bOXM8c_ObLiRfKgmWbacvva16jFLIXfv5CM0S2VA7Rhu90sdWbl7sljqu9lfbt9jklazQwOwwekL-_bg3tbXgeFAMY1stoD7fkJIVoP39w',
    'content-type': 'application/json',
    'origin': 'https://www.thredup.com',
    'referer': 'https://www.thredup.com/women/jeans?department_tags=women&category_tags=jeans',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'x-previous-referrer': 'https://www.thredup.com',
}

def post_request(URL, payload, headers, cookies):
    return requests.request("POST", URL, json=payload, headers=headers, cookies=cookies).json()

def json_variables(json_amount=119, json_page=2):
    payload_initial_products['variables']['amount'] = json_amount
    payload_initial_products['variables']['page'] = json_page
    
    
    
def get_initial_products(json_amount, max_page):
    #set payload and headers data for initial products
    data_initial_products = []
    start_time = time.time()
   
    for idx in range(1,max_page):
        print(f'Scraping Initial Products Page: {idx}', end='\r')
        json_variables(json_amount ,json_page=idx)
        time.sleep(1)
        try:
            data_initial_product = post_request(URL, payload_initial_products, headers, cookies)['data']['items']['nodes']
            if len(data_initial_product) == 0:
                print(idx, "There is no more products")
                break
            data_initial_products.append(data_initial_product)
        except Exception as e:
            print(f"\nError retrieving data_initial_product: {e} \n")
            pass
    
    end_time = time.time()
    print(f"Time taken to Scrape {idx} Pages: {end_time - start_time}")
    
    return data_initial_products

def parse_initial_products(data_initial_products):
    df_initial_product = pd.DataFrame()
    df_initial_products = pd.DataFrame()

    for data_initial_product in data_initial_products:
        df_initial_product = pd.DataFrame(data_initial_product)
        df_initial_products = pd.concat([df_initial_products, df_initial_product],ignore_index=True)
        
    print(f'There are: {df_initial_products["itemNumber"].duplicated().sum()} duplicated items in Data.')
    return df_initial_products[["itemNumber", "price"]]