from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
import datetime

import zmq
import dill
from io import BytesIO

import threading

import os

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
# Socket to talk to server

socket.connect ("tcp://localhost:5555" )

se = SystemSimulator()
se.register_engine("sname3", "REAL_TIME", 0.01)

class Process(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("PROCESS", 0)

        self.insert_input_port("process")
        self.message_list = []
        
    def ext_trans(self,port, msg):
        if port == "process":
            print("!")
            self.message_list.append(msg.retrieve())
            self._cur_state = "PROCESS"

    def output(self):
        print(self.message_list)
        self.message_list = []
        return None
        
    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"

def recv_thread():
    model_cnt = 0
    while True:
        msg = socket.recv()
        print(f"model receved")
        model = dill.temp.loadIO(BytesIO(msg))
        model.update_state("MOVE", 0.1)
        process = Process(0, Infinite, f"[PROC_{model_cnt}", "sname3")
        se.get_engine("sname3").register_entity(process)
        #for model in models:
        se.get_engine("sname3").register_entity(model)
        se.get_engine("sname3").coupling_relation(model, "process", process, "process")
 
t = threading.Thread(target=recv_thread, args=())
t.start()

while True:
    se.get_engine("sname3").simulate(1)
    #print(se.get_engine("sname3").get_global_time())
    migrate_models = se.get_engine("sname3").get_entity("Gen")
    #for model in migrate_models:
        #if model.is_migrate():
        #    se.get_engine("sname3").remove_entity("Gen")


###59 rec 받는 순간에 프로세스 모델을 추가 =>62 rec 모델추가 
### 63 추가한 모델이랑 rec 한 모델을 연결
### 3개 코드 합치면 과제의 시뮬레이션 파트는 끝  ==> AI 추후 연결
##모델이 오면 AI 파트랑 연결
##엣지서버에서 헬스 모델이 있는 것이랑 사람이 여러명있는 상황?
## 환경 heat : 환경 모델이 있고 거기 output port : heat ===== human model 이랑 연결하면
## heat 에서 msg 내보내면 모들 human 모델이 같은  msg를 받는다

