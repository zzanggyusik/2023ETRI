from pyevsim import BehaviorModelExecutor, Infinite
import sys, os
import zmq
import json

class MonitoringModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, engine, config):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.monitoring_engine = engine
        
        self.model_config = config["Model_config"]
        self.server_config = config["Server_config"]
        self.container_config = config["Container_config"]
        
        HOST_IP = self.server_config["host_ip"]
        HOST_PORT = self.server_config["host_port"]
        
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.connect(f'tcp://{HOST_IP}:{HOST_PORT}')
        
        self.client_name = os.getenv(self.container_config["container_name"])
        
        # Define State
        self.init_state("MONIT")
        self.insert_state('IDLE', Infinite)
        self.insert_state("MONIT", 1)
        
        # Define Port
        self.insert_input_port("monitoring_start")
        self.insert_input_port("monitoring_finish")
        
    def ext_trans(self, port, msg):
        if port == "monitor_start":
            self._cur_state = "MONIT"
            
        elif port == "monitor_finish":
            self._cur_state = "IDLE"
        
    def output(self):
        if self._cur_state == "MONIT":
            
            # Use path from config and monitor if file exist
            target_dir_path = self.model_config["monitor_target_path"]
            
            # Use for monitoring specific file
            target_file_type = self.model_config["monitor_target_file_type"]
            target_file = f'{self.client_name}{target_file_type}'
            
            print(f'Target file : {target_file}\nFile Exist : {target_file in (os.listdir(target_dir_path))}\n')
            
            # File Found
            if target_file in (os.listdir(target_dir_path)):
                self._cur_state = "IDLE"
                data = {
                    "client_name" : self.client_name,
                    "message" : "Task Done"
                }
                self.socket.send_string(json.dumps(data))
                print(f'Monitoring State : {data["message"]}')
                
    def int_trans(self):
        if self._cur_state == "MONIT":
            self._cur_state = "MONIT"
            
        elif self._cur_state == "IDLE":
            self._cur_state = "IDLE"