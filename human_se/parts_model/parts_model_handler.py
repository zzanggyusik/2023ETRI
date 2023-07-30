from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import os
import numpy as np
import zmq
import time

import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from config import *

class PartsModelHandler(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, engine):
            BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

            self.parts_engine = engine
            self.model_name = name
            
            # State 설정
            self.init_state(SimulationModelState.IDLE)
            self.insert_state(SimulationModelState.IDLE, Infinite)
            self.insert_state(SimulationModelState.PROCESS, 50000)
            self.insert_state(SimulationModelState.FINISH, 1)

            # Port 설정
            self.insert_input_port(SimulationPort.partsModelHandler_start)
            self.insert_input_port(SimulationPort.partsModelHandler_finish)
            
            self.insert_output_port(SimulationPort.partsModel_start)
            print("Parts Model Handler Start")
            print(SimulationPort.partsModelHandler_start)
            
            
    # 실행시 내부 진행때 사용하면될듯
    def ext_trans(self, port, msg):
        if port == SimulationPort.partsModelHandler_start:
            print("Parts Model Handler Start")
            self._cur_state = SimulationModelState.PROCESS
            
        elif port == SimulationPort.partsModelHandler_finish:
            self._cur_state = SimulationModelState.IDLE        
        
    # 데이터 전송시 사용하는 외부포트 (state, evt 적용)
    def output(self):
        if self._cur_state == SimulationModelState.PROCESS:
            msg = SysMessage(self.get_name(), SimulationPort.partsModel_start)
            
            return msg
            
            # self._cur_state = SimulationModelState.IDLE
                          
        
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
        url = f"tcp://*:{PartsModelPubPorts.stand.value}"
        self.publisher.bind(url)
        print(f"{self.model_name} Publish Start at {url}")
        
