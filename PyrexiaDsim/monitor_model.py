from pyevsim import BehaviorModelExecutor, Infinite
import sys, os
import zmq
import json
from datetime import datetime

class HumanModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, engine, config):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.monitoring_engine = engine
        
        self.pyrexiadsim_config = config["PyrexiaDsim_config"]
        self.model_config = self.pyrexiadsim_config["model_config"]
        
        self.generate_config = config["Virtual_config"]["generator_config"]
        self.monitor_config = config["Virtual_config"]["monitor_config"]
        self.container_config = config["Container_config"]
        
        # Monitor(local) IP/PORT
        MONITOR_IP = self.monitor_config["ip"]
        MONITOR_PORT = self.monitor_config["port"]
        # # Generate(virtual) IP/PORT
        # GENERATE_IP = self.generate_config["ip"]
        # GENERATE_PORT = self.generate_config["port"]
        
        self.context = zmq.Context() 
        
        self.mon_socket = self.context.socket(zmq.ROUTER)
        self.mon_socket.bind(f'tcp://{MONITOR_IP}:{MONITOR_PORT}')
        
        # Define State
        self.init_state("IDLE")
        self.insert_state('IDLE', Infinite)
        self.insert_state("MONIT", 1)
        
        # Define Port
        self.insert_input_port("monitor_model_start")
        self.insert_input_port("monitor_model_finish")
        
    def ext_trans(self, port, msg):
        if port == "monitor_model_start":
            self._cur_state = "MONIT"
        
            
        elif port == "monitor_model_finish":
            self._cur_state = "IDLE"
        
    def output(self):
        if self._cur_state == "MONIT":
            #TODO refer DB, Create Docker Container
            self.check_db()
    
            
        elif self._cur_state == "IDLE":
            print("IDLE")
                
    def int_trans(self):
        if self._cur_state == "MONIT":
            self._cur_state = "MONIT"
            
        elif self._cur_state == "IDLE":
            self._cur_state = "IDLE"   
        
    def check_db(self, config):
        # TODO : DB확인해서 Agent Container를 생성할지 확인하고 정보 전달
        
        data = {
            "human_id" : ""
            } # DB를 통해서 넘겨줄 데이터들
        
        self.run_containers(data, config)
        pass
        
    def run_gen_container(self, data, config):
        # TODO : Generator container 실행
        container_name = data["human_id"]
        container_image = self.container_config["generator_container_image"]
        try :
            os.system(f"docker run -d  -e CONTAINER_NAME={container_name} --name {container_name} {container_image}")
            print(f'Container {container_name} is Now Running')
        
        except:
            os.system(f"docker start {container_name}")
            print(f'Container {container_name} is Starting')
        