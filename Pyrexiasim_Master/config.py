from enum import Enum
#from instance.config import *

SITE = 'site1'

class Init():
    enmae = 'pyrexiasim'
    simulation_time = 'REAL_TIME'
    simulation_unit_time = 1
    
    model_manager_name = 'model_manager'
    telegram_manager_name = 'telegram_manager'

class SimulationPort():
    humanInfoModel_start = "humanModel_start"
    humanInfoModel_finish = "humanModel_finish"
    
    humanSimulation_start = "humanSimulation_start"
    humanSimulation_finish = ""
    #####################################################
    partsModelHandler_start = "partsModelHandler_start"
    partsModelHandler_finish = "partsModelHandler_finish"

    partsModel_start = "partsModel_start"
    partsModel_finish = "partsModel_finish"
    
class SimulationModelState():
    IDLE = "IDLE"
    PROCESS = "PROCESS"
    FINISH = "FINISH"
    
class WorkerFlushConfig():
    model_name = 'Flush'
    
    health_info_port = 'health_info'
    flush_port = 'flush'
    
    IDLE = 'IDLE'
    
class WorkerConfig():
    num_contariner = 5
    mount_dir_path = '/Users/qsiik/Desktop/2023ETRI/Pyrexiasim_Master/Results'
    
    client_img = 'zzanggyusik/agent_parts'
    
    router_ip = '*'
    router_port = 9999
    
class WorkerRemoveConfig():
    typevar = 'ModelManager'
    
    model_start_port = 'remove_worker'
    
    IDLE = 'IDLE'
    HANDLE = 'HANDLE'
    
class DBConfig():
    ip = '192.168.50.113'
    port = 27017
    id = ''
    pwd = ''
    
    human_db_name = 'pyrexiasim'
    site_db_name = 'env'
    
    human_info_collection = 'human_info'
    site_info_collection = 'site_info'
    
    
    #def get_human_info()
    
class TelegramConfig():
    token = '5853861114:AAHa1oCKnCukwT866Wm6rd8cWh7YL-pg3gA'
    
class PYZMQ():
    data_sender_host = "*"
    data_sender_port = 9898