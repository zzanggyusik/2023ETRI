from enum import Enum
#from instance.config import *
    
SITE = 'site1'   
    
class DBConfig():
    ip = '192.168.50.113'
    port = 27017
    id = ''
    pwd = ''
    
    human_db_name = 'pyrexiasim'
    site_db_name = 'env'
    
    human_info_collection = 'human_info'
    site_info_collection = 'site_info'
    
HUMAN_LIST = ['person1', 'person2']
    