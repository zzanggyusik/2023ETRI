from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import os
import numpy as np
from config import *


class HumanInfoModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, engine):
            BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

            self.ai_engine = engine
            
            # 상태 설정
            self.init_state(SimulationModelState.IDLE)
            self.insert_state(SimulationModelState.IDLE, Infinite)
            self.insert_state(SimulationModelState.PROCESS, 1)
            self.insert_state(SimulationModelState.FINISH, 1)

            # 포트 설정
            self.insert_input_port(SimulationPort.humanInfoModel_start)
            self.insert_input_port(SimulationPort.humanInfoModel_finish)
            
            self.insert_output_port("process")
            
    # 실행시 내부 진행때 사용하면될듯
    def ext_trans(self, port, msg):
        if port == SimulationPort.humanInfoModel_start:
            print(msg.retrieve()[0])
            self._cur_state = SimulationModelState.PROCESS
            
        elif port == SimulationPort.humanInfoModel_finish:
            self._cur_state = SimulationModelState.IDLE        
    
    # 데이터 전송시 사용하는 외부포트 (state, evt 적용)
    def output(self):
        if self._cur_state == SimulationModelState.PROCESS:
            print("HELLO There.")
            
            self._cur_state = SimulationModelState.IDLE
 
            # # 시나리오 수만큼 진행
            # if not self.level == self.scenario_length:
            
            #     self.level += 1
            #     print("----------------------------------------------------------")
            #     print(f"Scenario Processing! {self.level}")
                
            #     msg = SysMessage(engine_name = self.get_name(), out_port = "process")
            #     msg.insert({"scenario_length" : self.scenario_length , "current_level" : self.level, "img" : self.current_img})
                
            #     print("Scenario Model IDLE")
            #     self._cur_state = "IDLE"
                
            #     # print(msg)
            #     return msg
                
            
            # else:
            #     print(f"Scenario Action : {self.scenario_data}")
            #     print(f"Predicted Action : {self.model_predict}")
            #     print("Finish!")
            #     self._cur_state = "FIN"
                
            
        
    def int_trans(self):
        if self._cur_state == SimulationModelState.PROCESS:
            self._cur_state = SimulationModelState.PROCESS
            
        elif self._cur_state == SimulationModelState.IDLE:
            self._cur_state = SimulationModelState.IDLE
            
        elif self._cur_state == SimulationModelState.FINISH:
            self.ai_engine.simulation_stop()
