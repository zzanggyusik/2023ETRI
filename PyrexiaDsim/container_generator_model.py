from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import sys, os
import zmq
import json
from datetime import datetime
from config import *
from rest_api import RestApi
from threading import Thread
import time

class ContainerGeneratorModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, engine, human_info, human_profile, port):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        # Init Engine
        self.engine = engine
        self.port = port
        
        # Init ZMQ Socket
        self.context = zmq.Context()
        # self.dealer= self.zmq_dealer_init()
        self.router= self.zmq_router_init()
        
        # # Init MongoDB
        # self.mongo_client= MongoClient(MongoDBConfig.host, MongoDBConfig.port)
        self.mongo_api = RestApi()
        
        # Define State
        self.init_state(ContainerGeneratorConfig.PROCESSING)
        
        self.insert_state(ContainerGeneratorConfig.IDLE, Infinite)
        self.insert_state(ContainerGeneratorConfig.PROCESSING, 1)
        
        # Define Port
        self.insert_input_port(ContainerGeneratorConfig.start)
        self.insert_input_port(ContainerGeneratorConfig.fin)
        
        self.insert_output_port(ContainerGeneratorConfig.out)
        
        # Get Human Data
        self.human_info = human_info
        self.human_profile = human_profile
        
        self.db_insert_list= []
        
        self.instance_count= 0

        self.container_list = []
        
    def ext_trans(self, port, msg):
        if port == ContainerGeneratorConfig.start:
            self._cur_state = ContainerGeneratorConfig.PROCESSING
        
        elif port == ContainerGeneratorConfig.fin:
            self._cur_state = ContainerGeneratorConfig.IDLE
        
    def output(self):
        if self._cur_state == ContainerGeneratorConfig.PROCESSING:
            human_info_string= self.human_data_preprocessing()
            print(f'[Generator Model]: human_info_string = {human_info_string}')
            
            start_time = str(datetime.now().isoformat(timespec="seconds"))
                        
            # Create Agent Containers
            for i in range(PyrexiaDsimConfig.instance_number):
                agent_container_name = f'{self.human_info["human_id"]}_{i}_' + human_info_string
                self.container_list.append(agent_container_name)
                self.run_containers(agent_container_name)            
            
            self.check_container_instance(start_time)
            
            collection_name = start_time + "/" + self.human_info["human_id"]
            #self.mongo_client["pyrexiasim_log"][collection_name].insert_many(self.db_insert_list)
            for i in self.db_insert_list:
                self.mongo_api.post("pyrexiasim_log", collection_name, i)

            self.stop_containers()
            
            # Destroy ZMQ
            self.zmq_destroy()
            message = SysMessage(self.get_name(), ContainerGeneratorConfig.out)
            message.insert(self.get_name())
            
            return message
            
        elif self._cur_state == ContainerGeneratorConfig.IDLE:
            print("[Generator Model]: IDLE")
                
    def int_trans(self):
        if self._cur_state == ContainerGeneratorConfig.PROCESSING:
            self._cur_state = ContainerGeneratorConfig.IDLE
            
        elif self._cur_state == ContainerGeneratorConfig.IDLE:
            self._cur_state = ContainerGeneratorConfig.PROCESSING   
        
    def human_data_preprocessing(self):
        # DB에서 human_id에 해당하는 데이터 조회
        disease = None

        site_id= self.human_info["site_id"][6:]
        
        # Preprocessing Gender
        if self.human_profile["gender"] == "male":
            gender= Gender.MALE.value
        
        else:
            gender= Gender.FEMALE.value
        
        # Preprocessing Disease
        if self.human_profile["chronic_disease"] == "arthritis":
            disease= ChronicDisease.ARTHRITIS.value
            
        elif self.human_profile["chronic_disease"] == "hypertension":
            disease= ChronicDisease.HYPERTENSION.value
            
        elif self.human_profile["chronic_disease"] == "hypacusis":
            disease= ChronicDisease.HYPACUSIS.value
            
        elif self.human_profile["chronic_disease"] == "hyperthermia":
            disease= ChronicDisease.HYPERTHERMIA.value
            
        elif self.human_profile["chronic_disease"] == "diabetes-mellitus":
            disease= ChronicDisease.DIABETES_MELLITUS.value
        
        height= self.human_profile["height"]
        
        weight= self.human_profile["weight"]
        
        
        human_info_string= f"{self.human_info['worked_times']}_{site_id}_{self.human_info['health']}_{gender}_{disease}_{height}_{weight}_{self.human_info['heart_rate']}"
        
        return human_info_string
        
    def run_containers(self, agent_container_name): 
        agent_container_image = AgentContainerConfig.image_name
        try :
            os.system(f"sudo docker run -d -e CONTAINER_NAME={agent_container_name} -e PORT={self.port} --privileged --add-host host.docker.internal:host-gateway --name {agent_container_name} {agent_container_image}")
            print(f'[Generator Model]: Container {agent_container_name} is Now Running!!')

        except:
            os.system(f"sudo docker start {agent_container_name}")
            print(f'[Generator Model]: Container {agent_container_name} is Now Starting!!')
        
    def check_container_instance(self, start_time):
        while True:
            print("[Generator Model]: Router - Waiting...")
            identity, message = self.router.recv_multipart()
            message= json.loads(message.decode())
            if message['message'] == 'start':
                print(f'[Generator Model]: {identity} : {start_time}')
                self.router.send_multipart([identity, f"{start_time}".encode("utf-8")])
            
            if message['message'] == 'done':
                self.instance_count += 1
                self.db_insert_list.append(message["data"])
                
                print(f"{message['container_name']} --> Done")
            
                if self.instance_count == PyrexiaDsimConfig.instance_number:
                    print("[Generator Model]: All Container Created!")
                    break        
        
    def stop_containers(self) :
        for container_name in self.container_list:
            print(f"Removing {container_name}")
            os.system(f"sudo docker kill {container_name}") # Docker Stop
            os.system(f'sudo docker rm {container_name}')

        print(f'All Container Deleted')
        
    def zmq_dealer_init(self):
        socket = self.context.socket(zmq.DEALER)
        socket.connect(f"tcp://{ZMQ_NetworkConfig.generator_d_host}:{ZMQ_NetworkConfig.generator_d_port}")
        
        return socket                
    
    def zmq_router_init(self):
        socket = self.context.socket(zmq.ROUTER)
        socket.bind(f"tcp://{ZMQ_NetworkConfig.generator_r_host}:{self.port}")
        
        return socket
    
    def zmq_destroy(self):
        self.router.close()
        self.context.term()
