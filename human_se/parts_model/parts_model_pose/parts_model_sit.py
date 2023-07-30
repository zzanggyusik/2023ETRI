from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import os
import numpy as np
import zmq
import time

import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from config import *

class PartsModelSit(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, engine):
            BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

            self.ai_engine = engine
            self.model_name = name
            
            # State 설정
            self.init_state(SimulationModelState.IDLE)
            self.insert_state(SimulationModelState.IDLE, Infinite)
            self.insert_state(SimulationModelState.PROCESS, 1)
            self.insert_state(SimulationModelState.FINISH, 1)

            # Port 설정
            self.insert_input_port(SimulationPort.partsModel_start)
            self.insert_input_port(SimulationPort.partsModel_finish)
            
            self.insert_output_port("process")
            
            # Init Publihser
            self.zmq_init()
            
    # 실행시 내부 진행때 사용하면될듯
    def ext_trans(self, port, msg):
        if port == SimulationPort.partsModel_start:
            publish_msg = "-10"
            
            
            print(f"Publihsing... : {PartsModelPubPorts.sit.name}, {publish_msg}")
            self.publisher.send_string(f"{PartsModelPubPorts.sit.name}, {publish_msg}")

            
            # self._cur_state = SimulationModelState.PROCESS
            
        elif port == SimulationPort.humanInfoModel_finish:
            self._cur_state = SimulationModelState.IDLE        
        
    # 데이터 전송시 사용하는 외부포트 (state, evt 적용)
    def output(self):
        if self._cur_state == SimulationModelState.PROCESS:
            print("HELLO There.")
            
            self._cur_state = SimulationModelState.IDLE
                          
        
    def int_trans(self):
        if self._cur_state == SimulationModelState.PROCESS:
            self._cur_state = SimulationModelState.PROCESS
            
        elif self._cur_state == SimulationModelState.IDLE:
            self._cur_state = SimulationModelState.IDLE
            
        elif self._cur_state == SimulationModelState.FINISH:
            self.ai_engine.simulation_stop()
            
    def zmq_init(self):
        context = zmq.Context()
        self.publisher = context.socket(zmq.PUB)
        url = f"tcp://*:{PartsModelPubPorts.sit.value}"
        self.publisher.bind(url)
        print(f"{self.model_name} Publish Start at {url}")
        
