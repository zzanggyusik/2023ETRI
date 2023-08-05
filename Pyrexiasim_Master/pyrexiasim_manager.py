from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.system_simulator import SysExecutor
from pyevsim.definition import *

from worker import WorkerModel
from worker_monitor import WorkerMoniorModel
from worker_remove import WorkerRemoveModel
from worker_flush import WorkerFlushModel
from telegram_manager import TelegramManagerModel
from worker_data_sender import WorkerDataSender

from config import *

import pymongo

class ModelManager():
    def __init__(self, inst_t, dest_t, mname, ename, engine:SysExecutor, tmanager:TelegramManagerModel):
        self.engine = engine
        self.tele_manager = tmanager
        self.worker_info_map = {}
        
        self.worker_monitor_model = WorkerMoniorModel(inst_t, dest_t, mname, ename, self)
        self.worker_remove_model = WorkerRemoveModel(inst_t, dest_t, mname, ename, self)
        self.worker_flush_model = WorkerFlushModel(inst_t, dest_t, WorkerFlushConfig.model_name, ename)
        self.worker_data_sender = WorkerDataSender(inst_t, dest_t, mname, ename, self.worker_info_map)
        
        #self.db_url = f"mongodb://{DBConfig.ip}:{DBConfig.port}@{DBConfig.pwd}"
        self.db_url = f"mongodb://{DBConfig.ip}:{DBConfig.port}"
        
        self.human_info_db = pymongo.MongoClient(self.db_url)[DBConfig.human_db_name]
        self.site_info_db = pymongo.MongoClient(self.db_url)[DBConfig.site_db_name]
        
        self.engine.register_entity(self.worker_flush_model)
        self.engine.register_entity(self.worker_remove_model)
        self.engine.register_entity(self.worker_monitor_model)
        self.engine.register_entity(self.tele_manager)
        self.engine.register_entity(self.worker_data_sender)

    def check_worker_in_map(self, human_id) -> bool:
        if human_id in self.worker_info_map:
            return True
        
        else: return False

    def insert_worker(self, human_id):
        human_info = self.human_info_db[DBConfig.human_info_collection].find_one({'id':human_id})
        worker_model = WorkerModel(0, Infinite, human_info['id'], self.engine.get_name(), human_id)
        self.worker_info_map[human_info['id']] = worker_model
        
        #self.engine.insert_input_port(self.model_name)
        self.engine.register_entity(worker_model)

        # coupling relation 
        self.engine.coupling_relation(worker_model, human_info['id'], self.worker_remove_model, "remove_worker")
        self.engine.coupling_relation(worker_model, 'msg', self.tele_manager, 'alert')


        self.engine.coupling_relation(worker_model, "health_info", self.worker_flush_model, "health_info")
        # self.engine.coupling_relation(worker_model, human_info['id'], self.worker_flush_model, "flush")
        print(human_info)
        print('Inserting')
        pass

    def remove_worker(self, human_info):
        print(human_info)
        self.human_info_db[DBConfig.human_info_collection].update_one({'id':human_info['id']}, {'$set':human_info})
        self.engine.remove_entity(human_info['id'])
        del self.worker_info_map[human_info['id']]

        pass