from pyevsim import BehaviorModelExecutor, Infinite
import sys, os
import zmq
import json
from datetime import datetime
from config import *
from threading import Thread
import time
from container_generator_model import ContainerGeneratorModel
from rest_api import RestApi
import socket
import random
from pymongo import MongoClient

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
        #self.mongo_api = RestApi()
        
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
            del self.generator_map[model_name]
            
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
        #human_list = self.mongo_api.get_document("human", "human_info", 100)

        
        # Check if human's simulation_activate field is "True"
        for human_info in human_list:
            if human_info["simulation_activate"] == True:
                
                # Set simulation_active Flag to False
                self.mongo_client["human"]["human_info"].update_one({"human_id": human_info["human_id"]}, {"$set":{"simulation_activate": False}})
                #self.mongo_api.put('human','human_info', 'human_id', human_info['human_id'], {"simulation_activate": False})
                
                # Get Human Profile
                human_profile= self.mongo_client["human"]["human_profile"].find_one({"human_id": human_info["human_id"]})
                #human_profile_list = self.mongo_api.get('human', 'human_profile', 'human_id', human_info['human_id'])
                #for human in human_profile_list:
                #    if human["human_id"] == human_info["human_id"]:
                #        human_profile = human
                
                # Check Human_Info Map
                # Create Generator, Insert to Engine
                if human_info["human_id"] in self.generator_map:
                    print(f"[Monitor Model]: {human_info['human_id']} - Already Existed")
                else:
                    print(f"[Monitor Model]: {human_info['human_id']} - Simulation Activated")
                    self.insert_generator(human_info, human_profile)
    
        
    def insert_generator(self, human_info, human_profile):
        port = self.find_free_port()
        generator_model = ContainerGeneratorModel(0, Infinite, human_info['human_id'], self.engine.get_name(), self.engine, human_info, human_profile, port)
        self.generator_map[human_info["human_id"]]= generator_model
        
        #self.engine.insert_input_port(self.model_name)
        
        self.engine.register_entity(generator_model)
        print(f"{human_info['human_id']} - Generator Inserted, binded port = {port}")    
        self.engine.coupling_relation(generator_model, ContainerGeneratorConfig.out,\
            self, MonitorModelConfig.model_in)

    def find_free_port(self):
        while True:
            port = random.randint(30000, 40000)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            if result != 0:
                return port