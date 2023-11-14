import random
import zmq
import json
import os

def main(config):
    
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    
    cur_container_name = os.getenv(config["container_name"])
    generator_container_name = cur_container_name.split("_")[0]
    GEN_PORT = config["gen_port"]
    
    socket.connect(f'tcp://{generator_container_name}:{GEN_PORT}')
    
    first_message = {
        "message" : "ready",
        "name" : cur_container_name,
        "data" : ""
    }
    
    socket.send_string("ready")
    
    while True :
        message = socket.recv_multipart()
        
        _, content = message
        
        depth = message["depth"]
        # TODO depth 에 따라서 행동 계산(기존 Pyrexiasim worker.py에서 가져오기)
        
        
        # TODO 계산이 끝나면 finish messgae의 data{} 에 데이터 담아서 보내기
        finish_message = {
            "message" : "finish",
            "name" : cur_container_name,
            "data" : {}
        }
        
        socket.send_string(json.dumps(finish_message))
    
if __name__ == '__main__' :
    with open("./instance/config.json") as config:
        config = json.load(config)