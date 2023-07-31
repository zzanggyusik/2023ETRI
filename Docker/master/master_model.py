from pyevsim import BehaviorModelExecutor, Infinite
import sys, os
import zmq
import json
from datetime import datetime
from pymongo import MongoClient

class MasterModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, engine, config):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.monitoring_engine = engine
        
        self.simulation_config = config["Simulation_config"]
        self.model_config = self.simulation_config["model_config"]
        self.generate_config = config["Server_config"]["generate_config"]
        self.container_config = config["Container_config"]
        self.db_config = config["DB_config"]
        
        self.client = MongoClient(config['ip'], config['port'])
        self.db = self.client.pyrexiasim.human_info
        
        self.data = None
                
        #HOST_IP = self.generate_config["host_ip"]
        GENERATE_IP = self.generate_config["host_ip_test"]
        GENERATE_PORT = self.generate_config["host_port"]
        
        self.context = zmq.Context()
        self.host_socket = self.context.socket(zmq.ROUTER)
        self.host_socket.bind(f'tcp://{GENERATE_IP}:{GENERATE_PORT}') 
        
        self.client_name = os.getenv(self.container_config["container_name"])
                
        # Define State
        self.init_state("IDLE")
        self.insert_state('IDLE', Infinite)
        self.init_state('START', Infinite)
        self.insert_state("SIMULATE", 1)
        
        # Define Port
        self.insert_input_port("human_model_start")
        self.insert_input_port("human_model_finish")
        
    def ext_trans(self, port, msg):
        if port == "human_model_start":
            self.run_containers(self.parallel_config)
            
            while True :
                try:
                    self.data = self.db.find_one({'id' : 'person1'})
                    self._cur_state = "SIMULATE"
                    break
                    
                except:
                    pass
                               
        elif port == "human_model_finish":
            self._cur_state = "IDLE"
        
    def output(self):
        if self._cur_state == "SIMULATE":
            #TODO refer DB Data
            data = self.db.find_one({'id': 'person1'})
            self.par_socket.send_json(data)
            print(f'Data : {data}\nSend')
            
            # Use path from config and start simulation
            
            #TODO if human is not exist
            #if 
            #    self._cur_state = "IDLE"
            
        elif self._cur_state == "IDLE":
            print("IDLE")
                
    def int_trans(self):
        if self._cur_state == "SIMULATE":
            self._cur_state = "SIMULATE"
            
        elif self._cur_state == "IDLE":
            self._cur_state = "IDLE"   
            
    def run_containers(self, config):
        #start_timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        
        mount_dir = config["mount_dir_path"]
        
        #TODO Run Container
        client_num = config["client_num"]
        client_image = config['client_image']
        
        print("\n@@ Start Runing Containers ...")
        
        for i in range(len(client_num)):
            print(f'[{i}] : Container {client_num[i]} Starting...')
            container_name = f'client_{client_num[i]}'
            
            try :
                os.system(f"docker run -v {mount_dir}:/Result -d  -e CONTAINER_NAME={container_name} --name {container_name} {client_image}")
                #print(f'[{i}] : Container {container_name} is Now Running!!')

            except:
                os.system(f"docker start {container_name}")
                #print(f'[{i}] : Container {container_name} is Now Starting!!')
                
        print("\n@@ All container is Running !!!\n")
        