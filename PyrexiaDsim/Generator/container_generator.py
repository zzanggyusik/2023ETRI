import sys, os
from datetime import datetime
import zmq
import zmq.asyncio
import threading
import json
import asyncio
from config import *
from pymongo import MongoClient, DESCENDING
import time
from datetime import datetime

class ContainerGenerator():
    def __init__(self) -> None:
        # RUN Docker
        os.system(f"service docker start")
        
        self.dealer= self.zmq_dealer_init()
        self.router= self.zmq_router_init()
        
        self.mongo_client= MongoClient(MongoDBConfig.host, MongoDBConfig.port)
        self.cur_container_name = os.getenv(ContainerGeneratorConfig.get_container_name)
        self.instance_count= 0
        
        self.db_insert_list= []
        
    # TODO main에서는 시작과 동시에 local monitor에게 자신이 실행해야 할 instance수와 데이터를 받아서 실행한다
    def main(self):    

        ##### REVIEW: 생성된 container_generator 컨테이너가 monitor_model 모델에게 자기 생성됐다고 알려주는 것인지?
        ##### ANSWER: YES, monitor_model(local)에게 생성이 되었으며 해당하는 데이터(현재 human, state)전달받아서 실행함
        #####          해당 이유는 시뮬레이션이 트리거가 되어 예측이 필요한 경우 바로 컨테이너 제너레이터가 만들어지며 이때 데이터를 
        #####          전달할 수 있는 방법으로 zmq통신을 선택함(확장성을 위함). 
        
        # monitor_model에게 자신이 잘 생성됐음을 알림
        print("Dealer - report start")
        self.report_to_router()
        print("Dealer - report end")
        
        # DB에서 human의 데이터를 읽어 컨테이너 이름 형태로 전처리
        human_info_string= self.human_data_preprocessing(self.cur_container_name)
                
        # TODO : Received current data(human_data, state)
        
        # Create Agent Containers
        for i in range(PyrexiaDsimConfig.instance_number):
            agent_container_name = f'{self.cur_container_name}_{i}_' + human_info_string
            self.run_containers(agent_container_name)
            
        # Check Container Create Successfully.
        self.check_container_instance()
        
        # Insert Simulation Result
        collection_name= self.cur_container_name + datetime.now()
        self.mongo_client["pyrexiasim_log"][collection_name].insert_many(self.db_insert_list)
        
        # Finish Process
        self.stop_containers()
        
            
    def check_container_instance(self):
        while True:
            print("Router - Waiting...")
            identity, message = self.router.recv_multipart()
            message= json.loads(message.decode())
            self.db_insert_list.append(message)
            
            self.instance_count += 1
            
            if self.instance_count == PyrexiaDsimConfig.instance_number:
                print("All Container Created!")
                break
        
    
    
    def report_to_router(self):
        """
        Router에게 자신이 생겼음을 알림. Router에게 ready 메세지를 보내고, checked 메세지를 기다림.
        checked 메세지가 오면 컨테이너 생성 시작
        """
        first_message = {
            "container_name" : self.cur_container_name,
            "message" : "ready"
        }
        
        self.dealer.send_string(json.dumps(first_message))        
        print("Dealer - message send to router")
        
        while True:
            print("Dealer - Waiting...")
            received_message = self.dealer.recv_multipart()
            print(f'Dealer - From Host Monitor received : {received_message}')
            
            break
    
    
    def run_containers(self, agent_container_name): 
        agent_container_image = AgentContainerConfig.image_name
        
        
        ##### REVIEW: agnet_container를 생성할 떄 base model의 데이터를 전달하는 방법 고려 필요. ENV, CMD, 통신 등 ...
        ##### ANSWER: zmq통신을 사용해아될것으로 보임(generator - agent간의 통신 -> 이부분은 agent에 어느정도 고려가 되어있음).
        try :
            os.system(f"docker run -d -e CONTAINER_NAME={agent_container_name} --name {agent_container_name} {agent_container_image}")
            print(f'Container {agent_container_name} is Now Running!!')

        except:
            os.system(f"docker start {agent_container_name}")
            print(f'Container {agent_container_name} is Now Starting!!')
            
    def stop_containers(self, agent_container_name) :
        
        ##### REVIEW: 1회성 연산 컨테이너이기 때문에 stop보다 kill이 더 효율적일듯 함(속도, 메모리 측면에서)
        print(f'\nStopping {agent_container_name} ...')
        os.system(f"docker stop {agent_container_name}") # Docker Stop
        print(f'Deleting {agent_container_name}...')
        os.system(f'docker rm {agent_container_name}') # Docker rm
        print(f'{agent_container_name} Deleted!!\n')
            
    async def generator_server_open(self, config):
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
                self.stop_containers(content["name"])
                
    
    def human_data_preprocessing(self, human_id):
        # DB에서 human_id에 해당하는 데이터 조회
        disease = None
        human_info= self.mongo_client["human"]["human_info"].find_one({"human_id": human_id})
        human_profile= self.mongo_client["human"]["human_profile"].find_one({"human_id": human_id})

        # Preprocessing States
        worked_time= human_info["worked_times"].split(":")
        states= int(((8 * 60) - ((int(worked_time[0]) * 60) + int(worked_time[1]))) / 30)

        site_id= human_info["site_id"][6:]
        
        # Preprocessing Gender
        if human_profile["gender"] == "male":
            gender= Gender.MALE.value
        
        else:
            gender= Gender.FEMALE.value
        
        # Preprocessing Disease
        if human_profile["chronic_disease"] == "arthritis":
            disease= ChronicDisease.ARTHRITIS.value
            
        elif human_profile["chronic_disease"] == "hypertension":
            disease= ChronicDisease.HYPERTENSION.value
            
        elif human_profile["chronic_disease"] == "hypacusis":
            disease= ChronicDisease.HYPACUSIS.value
            
        elif human_profile["chronic_disease"] == "hyperthermia":
            disease= ChronicDisease.HYPERTHERMIA.value
            
        elif human_profile["chronic_disease"] == "diabetes-mellitus":
            disease= ChronicDisease.DIABETES_MELLITUS.value
        
        height= human_profile["height"]
        
        weight= human_profile["weight"]
        
        
        human_info_string= f"{states}_{site_id}_{human_info['health']}_{gender}_{disease}_{height}_{weight}"
        
        return human_info_string
        
    
    def zmq_dealer_init(self):
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        socket.connect(f"tcp://{ZMQ_NetworkConfig.generator_d_host}:{ZMQ_NetworkConfig.generator_d_port}")
        
        return socket                
    
    def zmq_router_init(self):
        context = zmq.Context()
        socket = context.socket(zmq.ROUTER)
        socket.bind(f"tcp://{ZMQ_NetworkConfig.generator_r_host}:{ZMQ_NetworkConfig.generator_r_port}")
        
        return socket


if __name__ == '__main__' :        
    try : 
        ContainerGenerator().main()
        
    except KeyboardInterrupt:
        print("Caught keyboard interrupt. Canceling tasks...")
        for task in asyncio.all_tasks():
            task.cancel()