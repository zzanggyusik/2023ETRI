from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.system_simulator import SystemSimulator
from pyevsim.system_message import SysMessage
from pyevsim.definition import *

from typing import TypeVar

from config import * 

import pymongo
import datetime
import logging
import time

ModelManager = TypeVar('ModelManager')
class WorkerModel(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, mname, ename, human_id):
        super().__init__(inst_t, dest_t, mname, ename)
        #Env DB

        #self.db_url = f"mongodb://{DBConfig.ip}:{DBConfig.port}@{DBConfig.pwd}"
        self.db_url = f"mongodb://{DBConfig.ip}:{DBConfig.port}"
        self.human_info_db = pymongo.MongoClient(self.db_url)[DBConfig.human_db_name]
        self.human_id = human_id

        # Model Management
        self.insert_input_port(mname)
        self.insert_output_port(mname)

        # Environment Management
        self.insert_input_port('env')
        self.insert_output_port('req_env')

        # Telegram Management
        self.insert_output_port("msg")
        self.insert_output_port("health_info b ")

        # State
        self.init_state("MONITOR")
        self.insert_state("REQ_ENV", 0)
        self.insert_state("WAIT", Infinite)
        self.insert_state("MONITOR", 1)

        # Domain Part
        self.engine = SystemSimulator.get_engine(ename)
        self.env_info = None
        self.timestamp = None

    def ext_trans(self, port, msg):
        if port == 'env':
            self.env_info = msg.retrieve()[0]
            self._cur_state = "MONITOR"
        
    
    def output(self):
        if self._cur_state == "REQ_ENV":
            return SysMessage(self.get_name(), "req_env")
        
        elif self._cur_state == "MONITOR":
            human_info = self.human_info_db[DBConfig.human_info_collection].find_one({'id':self.human_id})
            # TODO: Check Health
            #print(f"{self.get_name()} checking hsinfo")
            
            # TODO: update human_info, should update each field

            msg_lst = []
            # Check validity
            if human_info['exist'] == 0:
                ## Delete Worker Model
                msg = SysMessage(self.get_name(), self.get_name())
                # msg = SysMessage(self.get_name(), "health_info")
                msg.insert(human_info)
                msg_lst.append(msg)
                
            else:
                print("Human Detected")
                print("Container Created")
                
                msg = SysMessage(self.get_name(), "containermodel_start")
                # TODO : Create Container

                while True:
                    # TODO : Router Send Data, Wait Receive
                    pass 
                
                # self._cur_state = "WAIT"
    
    
        elif self._cur_state == "WAIT":
            print("Hello, Created container")
                
            
            #컨테이너 모니터로부터 종료 응답 대기 후 컨테이너 삭제

        return msg_lst



    def int_trans(self):
        if self._cur_state == "MONITOR":
            self._cur_state = "MONITOR"
        elif self._cur_state == "REQ_ENV":
            self._cur_state = "WAIT"
        elif self._cur_state == "WAIT":
            self._cur_state = "WAIT"
