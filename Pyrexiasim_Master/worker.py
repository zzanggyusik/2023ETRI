from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.system_simulator import SystemSimulator
from pyevsim.system_message import SysMessage
from pyevsim.definition import *

from typing import TypeVar
import zmq
import random
import sys, os
import json

from config import * 

import pymongo
import datetime
import logging
import time

ModelManager = TypeVar('ModelManager')
class WorkerModel(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, mname, ename, human_id):
        super().__init__(inst_t, dest_t, mname, ename)
        #Env DB

        #self.db_url = f"mongodb://{DBConfig.ip}:{DBConfig.port}@{DBConfig.pwd}"
        self.db_url = f"mongodb://{DBConfig.ip}:{DBConfig.port}"
        self.human_info_db = pymongo.MongoClient(self.db_url)[DBConfig.human_db_name]
        self.human_id = human_id
        
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.ROUTER)
        self.socket.bind(f'tcp://{WorkerConfig.router_ip}:{WorkerConfig.router_port}')
        
        print(f'\n@@{human_id} Router Bined tcp://{WorkerConfig.router_ip}:{WorkerConfig.router_port} Success!! @@')

        # Model Management
        self.insert_input_port(mname)
        self.insert_output_port(mname)

        # Environment Management
        self.insert_input_port('env')
        self.insert_output_port('req_env')

        # Telegram Management
        self.insert_output_port("msg")
        self.insert_output_port("health_info b ")

        # State
        self.init_state("MONITOR")
        self.insert_state("REQ_ENV", 0)
        self.insert_state("WAIT", Infinite)
        self.insert_state("MONITOR", 1)

        # Domain Part
        self.engine = SystemSimulator.get_engine(ename)
        self.env_info = None
        self.timestamp = None

    def ext_trans(self, port, msg):
        if port == 'env':
            self.env_info = msg.retrieve()[0]
            self._cur_state = "MONITOR"
        
    
    def output(self):
        if self._cur_state == "REQ_ENV":
            return SysMessage(self.get_name(), "req_env")
        
        elif self._cur_state == "MONITOR":
            human_info = self.human_info_db[DBConfig.human_info_collection].find_one({'id':self.human_id})
            # TODO: Check Health
            #print(f"{self.get_name()} checking hsinfo")
            
            # TODO: update human_info, should update each field

            msg_lst = []
            # Check validity
            if human_info['exist'] == 0 :
                ## Delete Worker Model
                msg = SysMessage(self.get_name(), self.get_name())
                msg.insert(human_info)
                msg_lst.append(msg)
                
            elif human_info['site'] == SITE:
                print("Human Detected")
                print("Container Created")
                
                msg = SysMessage(self.get_name(), "containermodel_start")
                # TODO : Create Container
                # TODO : Docker Multi Staging을 통한 이미지 경량화 필요
                
                self.container_state = self.run_containers(human_info['id'])

                while True:
                    # TODO : Router Send Data, Wait Receive
                    message =  self.socket.recv_multipart()
                    identity, content = message
                    
                    print(f'From Client Dealer {identity} Received Message : {message}')
                    
                    if content.decode() in self.container_state.keys():
                         self.container_state[content.decode()] = 1
                    response = {
                        'human_id' : human_info['id'],
                        'site_id' : 'site1'
                    }
                    self.socket.send_multipart([identity, json.dumps(response).encode()])
                    print(f'Sent to {content.decode()} : {response}')
                                           
                    if all(value == 1 for value in self.container_state.values()):
                        break
                                       
                while True:
                    print("Waiting Untill Task Done")
                    message = self.socket.recv_multipart()
                    identity, content = message
                    print(message)
                    print(content)
                    content = json.loads(content.decode())
                    container_name = content["client_name"]
                    response = 'OK'
                    self.socket.send_string(response)
                    monitor_state = content["message"]
                            
                    print(f'\nFrom {container_name} Dealer Received Message : {content}')
                    
                    if monitor_state == 'Task Done':
                        print(f'{container_name} monitor state : {monitor_state}')
                        #self.stop_container(container_name)
                        self.container_state[container_name] = 0
                        print(self.container_state)
                        
                    if all(value == 0 for value in self.container_state.values()):
                        for key, values in self.container_state.items():
                            self.stop_container(key)
                        break 
                            
                self._cur_state = "WAIT"
    
    
        elif self._cur_state == "WAIT":
            pass
            
                
            #컨테이너 모니터로부터 종료 응답 대기 후 컨테이너 삭제

        return msg_lst

    def int_trans(self):
        if self._cur_state == "MONITOR":
            self._cur_state = "MONITOR"
        elif self._cur_state == "REQ_ENV":
            self._cur_state = "WAIT"
        elif self._cur_state == "WAIT":
            self._cur_state = "WAIT"

    def run_containers(self, id):
        running_container = {}
        
        start_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                
        print('\n@@@@ Start Running Coniners...')

        dir_path = f'{WorkerConfig.mount_dir_path}/{id}_{start_timestamp}'
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        
        for i in range(WorkerConfig.num_contariner):
            try : 
                self.seed = random.randint(0,100)
                client_name = f'{id}_{self.seed}'
                os.system(f"docker run -v {dir_path}:/Result -d  -e CONTAINER_NAME={client_name} --name {client_name} {WorkerConfig.client_img}")
                
                # Container state 확인용
                running_container[client_name] = 0
                
            except :
                print(f'Already using seed {self.seed}')
        
        print("@@@@ All container Is Running !!!\n")
        
        return running_container
    
    def stop_container(self, container_name):
        print(f'\nKilling {container_name} ...')
        
        os.system(f"docker kill {container_name}") # Docker Stop
        
        print(f'Deleting {container_name}...')
        
        os.system(f'docker rm {container_name}') # Docker rm
        
        print(f'{container_name} Deleted!!\n')
    