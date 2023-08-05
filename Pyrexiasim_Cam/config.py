from enum import Enum
#from instance.config import *
    
class DBConfig():
    ip = 'localhost'
    port = 27017
    id = ''
    pwd = ''
    
    human_db_name = 'pyrexiasim'
    site_db_name = 'env'
    
    human_info_collection = 'human_info'
    site_info_collection = 'site_info'
    