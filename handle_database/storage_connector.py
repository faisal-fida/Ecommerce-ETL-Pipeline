from google.oauth2 import service_account
from google.cloud import storage
import json
# Construct a BigQuery client object.
import time
import pandas as pd


class CloudStorageConnector:
    def __init__(self, creds=None):
        self.bucket_name = "etl_batch_data"
        if creds:
            credentials = service_account.Credentials.from_service_account_file(
                creds, scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )

            self.client = storage.Client(credentials=credentials, project=credentials.project_id,)
        else:
            self.client = storage.Client()
    
    def insertToStorage(self, data,folder_name,file_name):
        
        newline_json = ''
        for row in data:
            newline_json = newline_json + json.dumps(row) + '\n'
        #print(newline_json)
        
        file_path =  folder_name+'/'+file_name
        
        print("Data extracted to folder: ", folder_name, file_name)

        self.client.get_bucket(self.bucket_name).blob(file_path).upload_from_string(newline_json)
        print("Data Inserted Successfully!")
        
    def insertDataframeToStorage(self, df,folder_name,file_name):
        
        
        file_path =  folder_name+'/'+file_name
        
        print("Data extracted to folder: ", folder_name, file_name)

        self.client.get_bucket(self.bucket_name).blob(file_path).upload_from_string(df.to_csv(index=False), 'text/csv')
        print("Data Inserted Successfully!")
    
    
    def insertBytesToStorage(self, string,folder_name,file_name):
        
        file_path =  folder_name+'/'+file_name
        
        print("Data extracted to folder: ", folder_name, file_name)
        
        self.client.get_bucket(self.bucket_name).blob(file_path).upload_from_string(string)
        print("Data Inserted Successfully!")
    
    def readFileBlob(self, folder_name, file_name):
        """Read a file from the bucket."""

        
        if not folder_name or folder_name == "":
            file_path = file_name    
        else:
            file_path = folder_name + "/" + file_name
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(file_path)
    
        # read as string
        read_output = blob.download_as_string()
        print("Read token from bucket")
        return read_output
    
