from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.system_simulator import SystemSimulator
from pyevsim.system_message import SysMessage
from pyevsim.definition import *

from typing import TypeVar
import random
import sys, os

from config import * 

import json
import pymongo
import datetime
import logging
import time
import zmq
import threading

class WorkerDataSender(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, mname, ename, worker_info_map):
        super().__init__(inst_t, dest_t, mname, ename)
        
        self.worker_info_map = worker_info_map
        
        self.db_url = f"mongodb://{DBConfig.ip}:{DBConfig.port}"
        self.human_info_db = pymongo.MongoClient(self.db_url)[DBConfig.human_db_name]        

        # Model Management
        self.insert_input_port("datasender_start")
        self.insert_output_port("datasender_finish")

        # State
        self.init_state("PROC")

        self.insert_state("IDLE", Infinite)
        self.insert_state("PROC", 1)

        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        pub_url = f"tcp://{PYZMQ.data_sender_host}:{PYZMQ.data_sender_port}"
        self.socket.bind(pub_url)

        print(f"Data Sender Init at {pub_url}")

    def ext_trans(self, port, msg):
        pass
        

    def output(self):
        publish = threading.Thread(target=self.zmq_publish)
        publish.start()
        
        self._cur_state = "IDLE"
        
    def int_trans(self):
        if self._cur_state == "IDLE":
            self._cur_state = "IDLE"
        elif self._cur_state == "PROC":
            self._cur_state == "PROC"

    def mogrify(self, topic, msg):
        return topic + ' ' + json.dumps(msg)
    
    def zmq_publish(self):
        while True:
            if self.worker_info_map is not None:
                for key in self.worker_info_map.keys():
                    human_info = self.human_info_db[DBConfig.human_info_collection].find_one({'id':key})
                    del human_info["_id"]
                    print(f"Published to {key} : {human_info}")
                    self.socket.send_string(self.mogrify(key, human_info))        
                    
            time.sleep(1)