from pyevsim import BehaviorModelExecutor, Infinite
import sys, os
import zmq
import json
from datetime import datetime
from config import *
from pymongo import MongoClient, DESCENDING

# For Test - Need Delete!
from Generator.container_generator import ContainerGenerator

class MonitorModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, engine):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        # Init Engine
        self.engine = engine
        
        # Init ZMQ Socket
        self.socket= self.zmq_init()
        
        # Init MongoDB
        self.mongo_client= MongoClient(MongoDBConfig.host, MongoDBConfig.port)
        
        # Define State
        self.init_state(MonitorModelConfig.IDLE)
        self.insert_state(MonitorModelConfig.IDLE, Infinite)
        self.insert_state(MonitorModelConfig.PROCESSING, 5)
        
        # Define Port
        self.insert_input_port(MonitorModelConfig.start)
        self.insert_input_port(MonitorModelConfig.fin)
        
    def ext_trans(self, port, msg):
        if port == MonitorModelConfig.start:
            self._cur_state = MonitorModelConfig.PROCESSING
        
        elif port == MonitorModelConfig.fin:
            self._cur_state = MonitorModelConfig.IDLE
        
    def output(self):
        if self._cur_state == MonitorModelConfig.PROCESSING:
            #TODO refer DB, Create Docker Container
            self.check_db()
    
        elif self._cur_state == MonitorModelConfig.IDLE:
            print("IDLE")
                
    def int_trans(self):
        if self._cur_state == MonitorModelConfig.PROCESSING:
            self._cur_state = MonitorModelConfig.PROCESSING
            
        elif self._cur_state == MonitorModelConfig.IDLE:
            self._cur_state = MonitorModelConfig.IDLE   
        
    def check_db(self):
        # TODO : DB확인해서 Agent Container를 생성할지 확인하고 정보 전달
        
        # Read DB
        human_list= self.mongo_client["human"]["human_info"].find()
        
        # Check if human's simulation_activate field is "True"
        for human in human_list:
            if human["simulation_activate"] == True:
                print(f"{human['human_id']} - Simulation Activated")
                
                # Create Container Generator
                self.run_gen_container(human['human_id'])
        
    def run_gen_container(self, human_id):
        # TODO : Generator container 실행
        # container_name = human_id
        # container_image = ContainerGeneratorConfig.image_name
        
        # try :
        #     os.system(f"docker run -d  -e CONTAINER_NAME={container_name} --name {container_name} {container_image}")
        #     print(f'Container {container_name} is Now Running')
        
        # except:
        #     os.system(f"docker start {container_name}")
        #     print(f'Container {container_name} is Starting')
        
        # For Test - Need Delete!
        ContainerGenerator.main(human_id)
                
        
    def zmq_init(self):
        context = zmq.Context() 
        socket = context.socket(zmq.ROUTER)
        socket.bind(f'tcp://{ZMQ_NetworkConfig.monitor_r_host}:{ZMQ_NetworkConfig.monitor_r_port}')
        
        return socket