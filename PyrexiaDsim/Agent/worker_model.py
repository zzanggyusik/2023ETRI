from pyevsim import BehaviorModelExecutor, Infinite
import sys, os
import zmq
import json
import random
from instance.config import *

class HumanModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, engine):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        # TESTING CODE
        self.cur_container_name = 'containertestingcode_1_8_2_77_0_3_177_78'.split('_')
        
        # REAL CODE
        # self.cur_container_name = os.getenv(ContainerConfig.container_name).split('_')
        
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
    
    def classifier(self, hp, site_open, site_cowork):
        prediction = ''
        
        if site_open == Site.OPEN_SPACE.value and site_cowork == Site.COOPERATION.value:
            if hp < 30 : prediction = Classifier.DANGEROUS
            elif hp < 50 : prediction = Classifier.WARNING
            else : prediction = Classifier.GOOD
            
        elif site_open == Site.OPEN_SPACE.value and site_cowork == Site.INDEPENDENT.value:
            if hp < 40 : prediction = Classifier.DANGEROUS
            elif hp < 60 : prediction = Classifier.WARNING
            else : prediction = Classifier.GOOD
            
        elif site_open == Site.CLOSE_SPACE.value and site_cowork == Site.COOPERATION.value:
            if hp < 35 : prediction = Classifier.DANGEROUS
            elif hp < 55 : prediction = Classifier.WARNING
            else : prediction = Classifier.GOOD
            
        elif site_open == Site.CLOSE_SPACE.value and site_cowork == Site.INDEPENDENT.value:
            if hp < 55 : prediction = Classifier.DANGEROUS
            elif hp < 75 : prediction = Classifier.WARNING
            else : prediction = Classifier.GOOD
            
        return prediction 
            
    
    def cal_health(self):
        #data = self.cur_container_name
        depth = float(self.cur_container_name[2]) # depth
        gen_site = float(self.cur_container_name[3])
        gen_hp = float(self.cur_container_name[4])
        gender = float(self.cur_container_name[5])
        disease = float(self.cur_container_name[6])
        height = float(self.cur_container_name[7])
        weight = float(self.cur_container_name[8])
        
        result = {}
            
        for i in range(int(depth)):
            data = {}
            if i == 0:
                cur_site = gen_site
                cur_hp = gen_hp
                
            else :
                cur_site = random.randint(1,5)
                
            # cur_site에 따른 변화 필요 met = pose 로 간주함
            workIntensity, wbgt, smock, met, noise, site_open, site_cowork = self.num_converter(cur_site)
            
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
                
            prediction = self.classifier(cur_hp, site_open, site_cowork)
            
            data[f"{cur_site}"] = cur_hp
            data[f"prediction"] = prediction
            
            result[f"{i}"] = data
            
            print(result)
        
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
    
    def num_converter(self, cur_site):
        if cur_site == 1:
            workIntensity = WorkIntensity.MANAGEABLE
            wbgt = Temperture.MILD
            smock = Smock.VERY_LIGHT
            pose = Pose.STANDING
            noise = Noise.SILENT
            site_open = Site.OPEN_SPACE
            site_cowork = Site.INDEPENDENT
        
        elif cur_site == 2:
            workIntensity = WorkIntensity.MODERATE
            wbgt = Temperture.WARM
            smock = Smock.MEDIUM
            pose = Pose.SITTING
            noise = Noise.MODERATE
            site_open = Site.OPEN_SPACE
            site_cowork = Site.COOPERATION
            
        elif cur_site == 3:
            workIntensity = WorkIntensity.EASY
            wbgt = Temperture.MILD
            smock = Smock.LIGHT
            pose = Pose.SITTING
            noise = Noise.QUIET
            site_open = Site.OPEN_SPACE
            site_cowork = Site.INDEPENDENT
            
        elif cur_site == 4:
            workIntensity = WorkIntensity.CHALLENGING
            wbgt = Temperture.HOT
            smock = Smock.HEAVY
            pose = Pose.STANDING
            noise = Noise.NOISY
            site_open = Site.CLOSE_SPACE
            site_cowork = Site.COOPERATION
            
        elif cur_site == 5:
            workIntensity = WorkIntensity.DIFFICULT
            wbgt = Temperture.SCORCHING
            smock = Smock.VERY_HEAVY
            pose = Pose.STANDING
            noise = Noise.LOUD
            site_open = Site.CLOSE_SPACE
            site_cowork = Site.INDEPENDENT
            
        # print(workIntensity.value)
        # print(type(workIntensity))
            
        return float(workIntensity.value), float(wbgt.value), float(smock.value), float(pose.value), float(noise.value), float(site_open.value), float(site_cowork.value)