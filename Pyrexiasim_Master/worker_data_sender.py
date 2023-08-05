from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.system_simulator import SystemSimulator
from pyevsim.system_message import SysMessage
from pyevsim.definition import *

from typing import TypeVar
import random
import sys, os

from config import * 

import pymongo
import datetime
import logging
import time
import zmq

class WorkerDataSender(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, mname, ename, worker_info_map):
        super().__init__(inst_t, dest_t, mname, ename)
        
        self.worker_info_map = worker_info_map
        

        # Model Management
        self.insert_input_port("datasender_start")
        self.insert_output_port("datasender_finish")

        # State
        self.init_state("PROC")

        self.insert_state("IDLE", Infinite)
        self.insert_state("PROC", 1)

        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://*:5556")


    def ext_trans(self, port, msg):
        pass
        

    def output(self):
        pass

    def int_trans(self):
        if self._cur_state == "IDLE":
            self._cur_state = "IDLE"
        elif self._cur_state == "PROC":
            self._cur_state == "PROC"

    