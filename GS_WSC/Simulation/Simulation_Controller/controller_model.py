from pyevsim import BehaviorModelExecutor, Infinite
import sys, os
import zmq
import json

class ControllerModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, engine, config):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.monitoring_engine = engine
        
        self.model_config = config["Model_config"]
        self.server_config = config["Server_config"]
        self.container_config = config["Container_config"]
        self.simulation_config = config["Simulation_config"]
        
        HOST_IP = self.server_config["host_ip"]
        CONTROL_PORT = self.server_config["controller_port"]
        
        self.context = zmq.Context()
        self.con_socket = self.context.socket(zmq.DEALER)
        self.con_socket.connect(f'tcp://{HOST_IP}:{CONTROL_PORT}') 
        
        #TODO Chaing direct ip to container name
        self.client_name = os.getenv(self.container_config["container_name"])
                
        self.con_socket.send_string(self.client_name) 
        
        # Define State
        self.init_state("IDLE")
        self.insert_state('IDLE', Infinite)
        self.insert_state("CONTROL", 1)
        
        # Define Port
        self.insert_input_port("controller_start")
        self.insert_input_port("controller_finish")
        
    def ext_trans(self, port, msg):
        if port == "controller_start":
            
            while(True):
                print("Receive Ready...")         
                
                try :
                    message = self.con_socket.recv()
                    data = json.loads(message.decode())
                    print(f'Recieved Data : {data}')
                    print("sim start")
                    print(f'{data["scenario"]} : {data["seed"]}')

                    os.system(f"python3 {self.simulation_config['simulation_path']} {data['scenario']} {data['seed']} {self.simulation_config['result_path']} {self.client_name}")
                    self._cur_state = "CONTROL"
                    break
                    
                except :
                    print("Simulation is not running...")
                    self.con_socket.send_string(self.client_name)
            
        elif port == "controller_finish":
            self._cur_state = "IDLE"
        
    def output(self):
        if self._cur_state == "CONTROL":
            print("Control Task Done")
            # Use path from config and start simulation
            self._cur_state = "IDLE"
            
        elif self._cur_state == "IDLE":
            print("IDLE")
                
    def int_trans(self):
        if self._cur_state == "CONTROL":
            self._cur_state = "CONTROL"
            
        elif self._cur_state == "IDLE":
            self._cur_state = "IDLE"   
        