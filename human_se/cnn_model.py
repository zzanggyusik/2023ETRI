from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import numpy as np
import cv2
class CNNModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, engine, data_object):
            BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
            
            self.ai_engine = engine
            
            # 상태 설정
            self.init_state("IDLE")
            self.insert_state("IDLE", Infinite)
            self.insert_state("PROC", 1)

            # 포트 설정
            self.insert_input_port("aimodel_start")

            self.action_array = []
            self.modelname = "CNNModel"
            self.model = load_model("./model/cnn0601.h5") # h5 file
            
    # 실행시 내부 진행때 사용하면될듯
    def ext_trans(self, port, msg):
        if port == "aimodel_start":
            self.data = msg.retrieve()[0]
            print(f"{self.modelname} : Level {self.data['current_level']}")
            
            X = self.data['img']
            X = cv2.resize(X, (64,64))
            X = X.astype('float32') / 255
            X = np.expand_dims(X, axis = 0)
            
            self.behaviour = self.predict_output(self.model.predict(X))
            self.action_array.append(self.behaviour)
            
            self._cur_state = "PROC"      

    def predict_output(self, pred_res):
        index = np.argmax(pred_res)
        
        if index == 0:
            signal = 'go'
        elif index == 1:
            signal = 'left'
        elif index == 2:
            signal = 'right'
        elif index == 3:
            signal = 'stop'
        
        return signal
    
    # 데이터 전송시 사용하는 외부포트 (state, evt 적용)
    def output(self):
        if self._cur_state == "PROC":
            msg = SysMessage(self.get_name(), "process")
            # if self.data["current_level"] == self.data["scenario_length"]:
            #     msg.insert({self.modelname : self.action_array})
            msg.insert({self.modelname : self.action_array})
            self._cur_state = "IDLE"
            
            return msg
        
        
    
            
    def int_trans(self):
        if self._cur_state == "PROC":
            self._cur_state = "PROC"
            
        elif self._cur_state == "IDLE":
            self._cur_state = "IDLE"
