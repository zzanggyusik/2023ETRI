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

socket.connect ("tcp://localhost:5556" )

#  Socket to talk to server
print("ZMQ PUB Mode: Binding Port 5557")
socket2 = context.socket(zmq.PUB)
socket2.bind("tcp://*:5557")

se = SystemSimulator()
se.register_engine("sname3", "REAL_TIME", 0.01)


def recv_thread():
    while True:
        msg = socket.recv()
        print(f"model receved")
        model = dill.temp.loadIO(BytesIO(msg))
        #for model in models:
        se.get_engine("sname3").register_entity(model)
 
t = threading.Thread(target=recv_thread, args=())
t.start()

while True:
    se.get_engine("sname3").simulate(1)
    #print(se.get_engine("sname3").get_global_time())
    migrate_models = se.get_engine("sname3").get_entity("Gen")
    for model in migrate_models:
        if model.is_migrate():
            model.increase_migration()
            dump = dill.temp.dumpIO(model)
            dump.seek(0)
            socket2.send(dump.read())
            se.get_engine("sname3").remove_entity("Gen")

## 32 - rec
## 38 : 모델등록  => 78(카메라에서 영상을 바로 넘겨준다 -> )
##77카메라에서 영상을 바로 넘겨준다 -> ) -> 이벤트
##79 - 39
