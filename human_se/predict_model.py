from pyevsim import BehaviorModelExecutor, Infinite
from data_object import DataObject


class PredictModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, engine, data_object):
            BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

            self.ai_engine = engine
            
            # 상태 설정
            self.init_state("IDLE")
            self.insert_state("IDLE", Infinite)
            self.insert_state("PROC", 1)

            # 포트 설정
            self.insert_input_port("start")
            self.insert_input_port("stop")
            
            self.data_object = data_object
            
            
    # 실행시 내부 진행때 사용하면될듯
    def ext_trans(self,port, msg):
        if port == "start":
            self._cur_state = "PROC"
            
        elif port == "stop":
            self._cur_state = "IDLE"


    
    # 데이터 전송시 사용하는 외부포트 (state, evt 적용)
    def output(self):
        if self._cur_state == "PROC":

            print(f"Scenario Processing! {self.data_object.level}")
            self.data_object.level += 1
            
            if self.data_object.level == 5:
                # self.data_object.set_level(0)
                print("Predicting Model Start!")
                self.ai_engine.insert_external_event("predict", "predict")
                
                print("Scenario Model IDLE")
                self._cur_state = "IDLE"
            
            # 모델 예측
            # 모델 형성
            
    
            
    def int_trans(self):
        if self._cur_state == "PROC":
            self._cur_state = "PROC"
            
        elif self._cur_state == "IDLE":
            self._cur_state = "IDLE"
