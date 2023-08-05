from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.system_simulator import SystemSimulator
from pyevsim.system_message import SysMessage
from pyevsim.definition import *

from config import *

from typing import TypeVar

import pymongo

import datetime

ModelManager = TypeVar('ModelManager')
class WorkerMoniorModel(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, mname, ename, mmanager:ModelManager):
        super().__init__(inst_t, dest_t, mname, ename)

        #self.db_url = f"mongodb://{DBConfig.ip}:{DBConfig.port}@{DBConfig.pwd}"
        self.db_url = f"mongodb://{DBConfig.ip}:{DBConfig.port}"
        self.human_info_db = pymongo.MongoClient(self.db_url)[DBConfig.human_db_name]
        
        # X
        self.insert_input_port(mname)
        
        # Y
        self.insert_output_port(mname)

        # State
        self.init_state("MONITOR")
        self.insert_state("MONITOR", 1)

        # Domain Part
        self.model_manager = mmanager

    def ext_trans(self, port, msg):
        if port == self.get_name():
            self._cur_state = "MONITOR"
            self.cancel_rescheduling()
        pass
    
    def output(self):
        # Get All Worker
        if self._cur_state == "MONITOR":
            cursor = self.human_info_db[DBConfig.human_info_collection].find({})
            for doc in cursor:
                if not self.model_manager.check_worker_in_map(doc['id']):
                    self.model_manager.insert_worker(doc['id'])
                    print(f'Insert Data {doc["id"]}')
            return None
        

    def int_trans(self):
        if self._cur_state == "MONITOR":
            self._cur_state = "MONITOR"

        pass