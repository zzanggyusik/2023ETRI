from pyevsim import BehaviorModelExecutor, Infinite


class MobileNetModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, engine, data_object):
            BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
            
            self.ai_engine = engine
            
            # 상태 설정
            self.init_state("IDLE")
            self.insert_state("IDLE", Infinite)
            self.insert_state("PROC", 1)

            # 포트 설정
            self.insert_input_port("aimodel_start")
            self.insert_input_port("aimodel_stop")
            self.insert_input_port("result")
            
            self.data_object = data_object
            self.count = 0
    
    # 실행시 내부 진행때 사용하면될듯
    def ext_trans(self,port, msg):
        if port == "aimodel_start":
            self._cur_state = "PROC"
            
        elif port == "aimodel_stop":
            self._cur_state = "IDLE"
            
        elif port == "result":
            pass


    
    # 데이터 전송시 사용하는 외부포트 (state, evt 적용)
    def output(self):
        if self._cur_state == "PROC":
            # print(f"Mobilenet Model Predicting! {self.count}")
            self.count += 1
            
            if self.count == 5:
                self.count = 0
                # print("Mobilenet Model Start!")
                
                # self.ai_engine.insert_external_event("scenario_start", "scenario_start")
                 
                # print("Mobilenet Model IDLE")
                self._cur_state = "IDLE"
            
            # 모델 예측
            # 모델 형성
            
    
            
    def int_trans(self):
        if self._cur_state == "PROC":
            self._cur_state = "PROC"
            
        elif self._cur_state == "IDLE":
            self._cur_state = "IDLE"
