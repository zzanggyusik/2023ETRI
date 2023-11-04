from pyevsim import BehaviorModelExecutor, Infinite
import sys, os
import zmq
import json
import random
from instance.config import *

class HumanModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, engine):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.cur_container_name = os.getenv(ContainerConfig.container_name).split('_')
        
        # Define State
        self.init_state(SimulationModelState.IDLE)
        self.insert_state(SimulationModelState.IDLE, Infinite)
        self.insert_state(SimulationModelState.PROCESS, 1)
        
        # Define Port
        self.insert_input_port(SimulationConfig.workerModel_start)
        self.insert_input_port(SimulationConfig.workerModel_finish)
        
    def ext_trans(self, port, msg):
        if port == SimulationConfig.workerModel_start:
            self._cur_state = SimulationModelState.PROCESS
        
            
        elif port == SimulationConfig.workerModel_finish:
            self._cur_state = SimulationModelState.IDLE
        
    def output(self):
        if self._cur_state == SimulationModelState.PROCESS:
            #TODO refer DB, Create Docker Container
            data = self.cal_health()
            self.send_result(data)
            
        elif self._cur_state == SimulationModelState.IDLE:
            print(SimulationModelState.IDLE)
                
    def int_trans(self):
        if self._cur_state == SimulationModelState.PROCESS:
            self._cur_state = SimulationModelState.PROCESS
            
        elif self._cur_state == SimulationModelState.IDLE:
            self._cur_state = SimulationModelState.IDLE   
            
    def cal_health(self):
        #data = self.cur_container_name
        depth = int(self.cur_container_name[2]) # depth
        gen_site = int(self.cur_container_name[3])
        gen_hp = int(self.cur_container_name[4])
        height = int(self.cur_container_name[5])
        weight = int(self.cur_container_name[6])
        
        result = {}
            
        for i in range(depth):
            data = {}
            if i == 0:
                cur_site = gen_site
                cur_hp = gen_hp
                
            else :
                cur_site = random.randint(1,5)
                
            # TODO : site, smock, pose, wbgt mapping
            # TODO : personaliry data mapping
            
            # cur_site에 따른 변화 필요
            gender = 0
            smock = 0
            wbgt = 0
            met = 0
            disease = 0
            
            if gender == 0 :
                if disease == "당뇨" and met == "강도 4":
                    cur_hp -= 0.9*smock + 1*met*1.2 + 1.1*wbgt
                    
                elif disease == "고혈압" and met == "강도 5":
                    cur_hp -= 0.9*smock + 1*met*1.3 + 1.1*wbgt*1.1
                    
                elif disease == "난청" and cur_site == "소음심한곳":
                    cur_hp -= (0.9*smock + 1*met + 1.1*wbgt)*1.2
                
                elif disease == "열중증" and wbgt == "온도 높은곳":
                    cur_hp -= 0.9*smock + 1*met + 1.1*wbgt*1.3
                    
                elif disease == "관절염" and cur_site == "앉았다 일어나는곳":
                    cur_hp -= (0.9*smock + 1*met + 1.1*wbgt)*1.1
                    
                else :
                    cur_hp -= 0.9*smock + 1*met + 1.1*wbgt
                
            else :
                cur_hp -= 1.1*smock + 1.2*met + 1.3*wbgt
                
                if disease == "당뇨" and met == "강도 4":
                    cur_hp -= 1.1*smock + 1.2*met*1.2 + 1.3*wbgt
                    
                elif disease == "고혈압" and met == "강도 5":
                    cur_hp -= 1.1*smock + 1.2*met*1.3 + 1.3*wbgt*1.1
                    
                elif disease == "난청" and cur_site == "소음심한곳":
                    cur_hp -= (1.1*smock + 1.2*met + 1.3*wbgt)*1.2
                
                elif disease == "열중증" and wbgt == "온도 높은곳":
                    cur_hp -= 1.1*smock + 1.2*met + 1.3*wbgt*1.3
                    
                elif disease == "관절염" and cur_site == "앉았다 일어나는곳":
                    cur_hp -= (1.1*smock + 1.2*met + 1.3*wbgt)*1.1
                    
                else :
                    cur_hp -= 1.1*smock + 1.2*met + 1.3*wbgt
                
                
            
            data[f'{cur_site}'] = cur_hp
            
            result[f'{i}'] = data
        
        return result
        
    
    def send_result(self, data):
        HOST_IP = self.cur_container_name[0]
        HOST_PORT = ContainerConfig.HOST_PORT
        
        context = zmq.Context()
        
        worker_socket =context.socket(zmq.DEALER)
        worker_socket.connect()
        
        message = {
            "message" : 'finish',
            "data" : data
        }
        
        worker_socket.send_string(json.dumps(message))
    
        