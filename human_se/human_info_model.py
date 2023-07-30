from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import os
import numpy as np

class HumanInfoModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, engine):
            BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

            self.ai_engine = engine
            
            # 상태 설정
            self.init_state("IDLE")
            self.insert_state("IDLE", Infinite)
            self.insert_state("PROC", 1)
            self.insert_state("FIN", 1)

            # 포트 설정
            self.insert_input_port("scenario_start")
            self.insert_input_port("scenario_finish")
            
            self.insert_output_port("process")
        
            # self.scenario_data = [] # 시나리오 레이블
            # self.model_predict = {} # 모델 예측 결과
            
            # self.current_img = 0 # 현재 시나리오에서 진행중인 이미지
            # self.level = 0 # 현재 시나리오 단계
            # self.model_count = self.model_len # 추론이 완료된 모델 수 카운트
            
            # # Get scenario label
            # for i in self.scenario:
            #     self.scenario_data.append(i.split(".")[0])
            
            # self.scenario_length = len(self.scenario)
            
            # print(f"Scenario Model Activated!\nCurrent scenario length = {self.scenario_length}")
            # print(f"Num of Models Detected = {self.model_len}")
            
            
    # 실행시 내부 진행때 사용하면될듯
    def ext_trans(self, port, msg):
        if port == "scenario_start":
            if msg.retrieve()[0] != "scenario_start":
                    
                self.model_count += 1
                self.model_predict.update(msg.retrieve()[0])

            if self.model_count >= self.model_len:
                print(f"All model({self.model_count}) Predicted")
                self.model_count = 0
                self._cur_state = "PROC"
            
        elif port == "scenario_finish":
            self._cur_state = "IDLE"


    
    # 데이터 전송시 사용하는 외부포트 (state, evt 적용)
    def output(self):
        if self._cur_state == "PROC":
            
            # 시나리오 수만큼 진행
            if not self.level == self.scenario_length:
            
                self.level += 1
                print("----------------------------------------------------------")
                print(f"Scenario Processing! {self.level}")
                
                msg = SysMessage(engine_name = self.get_name(), out_port = "process")
                msg.insert({"scenario_length" : self.scenario_length , "current_level" : self.level, "img" : self.current_img})
                
                print("Scenario Model IDLE")
                self._cur_state = "IDLE"
                
                # print(msg)
                return msg
                
            
            else:
                print(f"Scenario Action : {self.scenario_data}")
                print(f"Predicted Action : {self.model_predict}")
                print("Finish!")
                self._cur_state = "FIN"
                
            
        
    def int_trans(self):
        if self._cur_state == "PROC":
            self._cur_state = "PROC"
            
        elif self._cur_state == "IDLE":
            self._cur_state = "IDLE"
            
        elif self._cur_state == "FIN":
            self.ai_engine.simulation_stop()
