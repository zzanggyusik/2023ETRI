import requests
import json
from config import *

class RestApi():
    def __init__(self):
        self.host = MongoDBConfig.host_url
        
    def get_document(self, db_name, col_name, limit):

        url = f"{self.host}/rest/1.0/mongodb/document?databaseName={db_name}&collectionName={col_name}&limit={limit}"

        res = requests.get(url)
        res = json.loads(res.text)
        
        return res

    
    def get(self, db_name, col_name, id_type, id):
        if id == '':
            URL = f'{self.host}/rest/1.0/{db_name}/{col_name}'
        else :
            URL = f'{self.host}/rest/1.0/mongodb/document?databaseName={db_name}&collectionName={col_name}&limit=100&condition=%7B%7D'
        res = requests.get(URL)
        res = json.loads(res.text)
        
        return res
        
    def post(self, db_name, col_name, data):
        URL = f'{self.host}/rest/1.0/mongodb/document?databaseName={db_name}&collectionName={col_name}'
        headers = {'Content-Type': 'application/json; chearset=utf-8'}
        
        res = requests.post(URL, data=json.dumps(data), headers=headers)
        
        return res
    
    def delete(self, db_name, col_name, id_type, id):
        URL = f'{self.host}/rest/1.0/{db_name}/{col_name}?{id_type}={id}'
        res = requests.delete(URL)
        
        return res

    def put(self, db_name, col_name, id_type, id, data):
        URL = f'{self.host}/rest/1.0/{db_name}/{col_name}?{id_type}={id}'
        headers = {'Content-Type': 'application/json; chearset=utf-8'}
        
        res = requests.put(URL, data=json.dumps(data), headers=headers)
        
        return res

    def post_log(self, db_name, log_name, data):
        URL = f'{self.host}/rest/1.0/mongodb/document?databaseName={db_name}&collectionName={log_name}'
        headers = {'Content-Type': 'application/json; chearset=utf-8'}
        
        res = requests.post(URL, data=json.dumps(data), headers=headers)
        
        return res

    def get_log(self,db_name, log_name, limit):
        URL = f'{self.host}/rest/1.0/mongodb/document?databaseName={db_name}&collectionName={log_name}&limit={limit}&condition=%7B%7D'
        res = requests.get(URL)
        res = json.loads(res.text)
        
        return res  

    def get_col(self):
        URL = f'{self.host}/rest/1.0/mongodb/collection?databaseName=pyrexiasim'
        res = requests.get(URL)
        res = json.loads(res.text)
        
        return res

    def get_collection(self, db_name):
        #URL = HOST + '/rest/1.0/' + db_name + '/' + col_name + '?' + id_name + '=' + id
        URL = f'{self.host}/rest/1.0/mongodb/collection?databaseName={db_name}'
        res = requests.get(URL)
        res = json.loads(res.text)
        
        return res
