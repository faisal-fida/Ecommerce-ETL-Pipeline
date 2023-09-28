from algoliasearch.search_client import SearchClient

# import os
# api_key = os.environ.get('API_KEY')
# app_id = os.environ.get('APP_ID')

# fake account
app_id = 'app_id'
api_key = 'api_key'
client = SearchClient.create(app_id, api_key)


def db_upload(dataJson):
    print("Adding data to Agolio DB..", sep='\r')
    index = client.init_index('thredup')
    response = index.save_objects(dataJson)
    print(response)
