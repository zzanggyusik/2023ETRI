from pyevsim import BehaviorModelExecutor, Infinite
import sys, os
import zmq
import json
from datetime import datetime
from config import *
from pymongo import MongoClient, DESCENDING
from threading import Thread
import time
from container_generator_model import ContainerGeneratorModel
from rest_api import RestApi

# For Test - Need Delete!
from Generator.container_generator import ContainerGenerator

class MonitorModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, engine):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        # Init Engine
        self.engine = engine
        
        # # Init ZMQ Socket
        # self.router= self.zmq_init()
        
        self.generator_map= {}
        
        # Init MongoDB
        self.mongo_client= MongoClient(MongoDBConfig.host, MongoDBConfig.port)
        # self.mongo_api = RestApi()
        
        # Define State
        self.init_state(MonitorModelConfig.IDLE)
        self.insert_state(MonitorModelConfig.IDLE, Infinite)
        self.insert_state(MonitorModelConfig.PROCESSING, 1)
        
        # Define Port
        self.insert_input_port(MonitorModelConfig.model_in)
        self.insert_input_port(MonitorModelConfig.start)
        self.insert_input_port(MonitorModelConfig.fin)
        
    def ext_trans(self, port, msg):
        if port == MonitorModelConfig.start:
            self._cur_state = MonitorModelConfig.PROCESSING
        
        elif port == MonitorModelConfig.model_in:
            
            # Remove Container Generator Model
            model_name = msg.retrieve()[0]
            self.engine.remove_entity(model_name)
            self._cur_state = MonitorModelConfig.PROCESSING
        
        elif port == MonitorModelConfig.fin:
            self._cur_state = MonitorModelConfig.IDLE
        
    def output(self):
        if self._cur_state == MonitorModelConfig.PROCESSING:
            #TODO refer DB, Create Docker Container
            self.check_db()

            # self._cur_state = MonitorModelConfig.IDLE
            
        elif self._cur_state == MonitorModelConfig.IDLE:
            print("IDLE")
                
    def int_trans(self):
        if self._cur_state == MonitorModelConfig.PROCESSING:
            self._cur_state = MonitorModelConfig.PROCESSING
            
        elif self._cur_state == MonitorModelConfig.IDLE:
            self._cur_state = MonitorModelConfig.IDLE   
        
    def check_db(self):
        # TODO : DB확인해서 Agent Container를 생성할지 확인하고 정보 전달
        print("[Monitor Model]: Monitoring DB...")
        # Read DB
        human_list= self.mongo_client["human"]["human_info"].find()
        # human_list = self.mongo_api.get_document("human", "human_info", 100)

        
        # Check if human's simulation_activate field is "True"
        for human_info in human_list:
            if human_info["simulation_activate"] == True:
                
                # Set simulation_active Flag to False
                self.mongo_client["human"]["human_info"].update_one({"human_id": human_info["human_id"]}, {"$set":{"simulation_activate": False}})
                # self.mongo_api.put('human','human_info', 'human_id', human_info['human_id'], {"simulation_activate": False})
                
                # Get Human Profile
                human_profile= self.mongo_client["human"]["human_profile"].find_one({"human_id": human_info["human_id"]})
                # human_profile = self.mongo_api.get('human', 'human_profile', 'human_id', human_info['human_id'])
                
                
                # Check Human_Info Map
                
                # Create Generator, Insert to Engine
                if human_info["human_id"] in self.generator_map:
                    print(f"[Monitor Model]: {human_info['human_id']} - Already Existed")
                else:
                    print(f"[Monitor Model]: {human_info['human_id']} - Simulation Activated")
                    self.insert_generator(human_info, human_profile)
                
                # Create Container Generator Model
                
                # Create Container Generator
                # self.run_gen_container(human['human_id'])
        
    def insert_generator(self, human_info, human_profile):
        generator_model = ContainerGeneratorModel(0, Infinite, human_info['human_id'], self.engine.get_name(), self.engine, human_info, human_profile)
        self.generator_map[human_info["human_id"]]= generator_model
        
        #self.engine.insert_input_port(self.model_name)
        
        self.engine.register_entity(generator_model)
        print(f"{human_info['human_id']} - Generator Inserted")    
        self.engine.coupling_relation(generator_model, ContainerGeneratorConfig.out,\
            self, MonitorModelConfig.model_in)

        # coupling relation 
        # self.engine.coupling_relation(generator_model, human_info['id'], self.worker_remove_model, "remove_worker")
        # self.engine.coupling_relation(generator_model, 'msg', self.tele_manager, 'alert')


        # self.engine.coupling_relation(worker_model, "health_info", self.worker_flush_model, "health_info")
        # self.engine.coupling_relation(worker_model, human_info['id'], self.worker_flush_model, "flush")

                
    
                
                
    ### CASE 1. Docker In Docker
    
    # def run_gen_container(self, human_id):
    #     # TODO : Generator container 실행
    #     container_name = human_id
    #     container_image = ContainerGeneratorConfig.image_name
        
    #     try :
    #         os.system(f"docker run -d -e CONTAINER_NAME={container_name} --privileged --name {container_name} {container_image}")
    #         print(f'Container {container_name} is Now Running')
        
    #     except:
    #         os.system(f"docker start {container_name}")
    #         print(f'Container {container_name} is Starting')
        
    #     # For Test - Need Delete!
    #     # Thread(target= ContainerGenerator().main, args= (human_id, )).start()
        
    #     while True:
    #         print("Router - Waiting...")
    #         identity, message = self.router.recv_multipart()
            
    #         message= json.loads(message.decode())
    #         print(f"From Dealer - {message['container_name']} : {message['message']}")
            
    #         break
        
    #     time.sleep(3)
    #     self.router.send_multipart([identity, "checked".encode("utf-8")])
    #     print("Router - Container Generator Checked")
        
    # def zmq_init(self):
    #     context = zmq.Context() 
    #     router = context.socket(zmq.ROUTER)
    #     router.bind(f'tcp://{ZMQ_NetworkConfig.monitor_r_host}:{ZMQ_NetworkConfig.monitor_r_port}')
        
    #     return router