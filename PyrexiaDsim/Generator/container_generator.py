import sys, os
from datetime import datetime
import zmq
import zmq.asyncio
import threading
import json
import asyncio


# TODO main에서는 시작과 동시에 local monitor에게 자신이 실행해야 할 instance수와 데이터를 받아서 실행한다
async def main(config):
    HOST_IP = config["host_ip"]
    HOST_PORT = config["host_port"]
    
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.DEALER)
    socket.connect(f"tcp://{HOST_IP}:{HOST_PORT}")
    
    cur_container_name = os.getenv(config["Container_config"]["container_name"])
    
    first_message = {
        "container_name" : cur_container_name,
        "message" : "ready"
    }
    
    ##### REVIEW: 생성된 container_generator 컨테이너가 monitor_model 모델에게 자기 생성됐다고 알려주는 것인지?
    
    socket.send_string(json.dumps(first_message))
    
    while True :
        received_message = await socket.recv_multipart()
        print(f'From Host Monitor received : {received_message}')
        
        identity, content = received_message
        ### REVIEW : message를 RECEIVE 받으면 while 루프 탈출 필요할듯
        
        
        # TODO : Received current data(human_data, state)
        instance_num = config["Generator_config"]["instance_num"]  
        for i in range(instance_num):
            agent_container_name = f'{cur_container_name}_{i}'
            run_containers(agent_container_name)            
        
        
async def run_containers(agent_container_name): 
    agent_container_image = config["Container_config"]["agent_container_image"]
    
    
    ##### REVIEW: agnet_container를 생성할 떄 base model의 데이터를 전달하는 방법 고려 필요. ENV, CMD, 통신 등 ...
    try :
        os.system(f"docker run -e CONTAINER_NAME={agent_container_name} --name {agent_container_name} {agent_container_image}")
        print(f'Container {agent_container_name} is Now Running!!')

    except:
        os.system(f"docker start {agent_container_name}")
        print(f'Container {agent_container_name} is Now Starting!!')
        
async def stop_containers(agent_container_name) :
    
    ##### REVIEW: 1회성 연산 컨테이너이기 때문에 stop보다 kill이 더 효율적일듯 함(속도, 메모리 측면에서)
    print(f'\nStopping {agent_container_name} ...')
    os.system(f"docker stop {agent_container_name}") # Docker Stop
    print(f'Deleting {agent_container_name}...')
    os.system(f'docker rm {agent_container_name}') # Docker rm
    print(f'{agent_container_name} Deleted!!\n')
        
async def generator_server_open(config):
    GEN_IP = config["Generator_config"]["ip"]
    GEN_PORT = config["Generator_config"]["port"]
    
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.ROUTER)
    socket.bind(f'tcp://{GEN_IP}:{GEN_PORT}')
    
    while True :
        agent_message = await socket.recv_multipart()
        
        # TODO : Agent 로부터 message 받았을때 어떠한 행동을 할지. 한번에? 아니면 리스트나 json에 append해서 한방에 db에 쏠지
        
        identity, content = agent_message
        
        # depth 와 같은 데이터 동적으로 변경할 수 있도록 하기
        if content["message"] == "ready" :
            starting_message = {
                "depth" : 8
            }
            
            socket.send_string(json.dumps(starting_message))
            
        elif content["message"] == "finish" :
            stop_containers(content["name"])
    

if __name__ == '__main__' :
    with open("./instance/config.json") as config:
        config = json.load(config)
        
    loop = asyncio.get_event_loop()

    start_event = asyncio.Event()
    stop_event = asyncio.Event()
    
    try : 
        loop.run_until_complete(main(config, start_event, stop_event))
        
    except KeyboardInterrupt:
        print("Caught keyboard interrupt. Canceling tasks...")
        for task in asyncio.all_tasks():
            task.cancel()
            
    finally:
        loop.close()