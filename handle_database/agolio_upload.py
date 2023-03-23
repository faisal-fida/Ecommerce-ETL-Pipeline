from algoliasearch.search_client import SearchClient

# import os
# api_key = os.environ.get('API_KEY')
# app_id = os.environ.get('APP_ID')

# fake account
app_id = 'YBZD8YE4C1'
api_key = 'cc6a72904286c34a09c5338cf400bfb8'
client = SearchClient.create(app_id, api_key)


def db_upload(dataJson):
    print("Adding data to Agolio DB..", sep='\r')
    index = client.init_index('thredup')
    response = index.save_objects(dataJson)
    print(response)
