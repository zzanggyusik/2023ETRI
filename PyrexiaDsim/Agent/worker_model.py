from pyevsim import BehaviorModelExecutor, Infinite
import sys, os
import zmq
import json
import random
from instance.config import *

class HumanModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, engine, human_info):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
    
        self.human_info= human_info
        
        self.dealer= self.zmq_init()
        
        # Define State
        self.init_state(SimulationModelState.IDLE)
        self.insert_state(SimulationModelState.IDLE, Infinite)
        self.insert_state(SimulationModelState.PROCESS, 1)
        
        # Define Port
        self.insert_input_port(SimulationConfig.workerModel_start)
        self.insert_input_port(SimulationConfig.workerModel_finish)
        
        # Init State
        self.cur_state_level= 1
        
        # Init Data
        self.simulation_log= []
        self.result_data= {}
        
    def int_trans(self):
        if self._cur_state == SimulationModelState.PROCESS:
            self._cur_state = SimulationModelState.PROCESS
            
        elif self._cur_state == SimulationModelState.IDLE:
            self._cur_state = SimulationModelState.IDLE   
        
    def ext_trans(self, port, msg):
        if port == SimulationConfig.workerModel_start:
            self._cur_state = SimulationModelState.PROCESS
         
        elif port == SimulationConfig.workerModel_finish:
            self._cur_state = SimulationModelState.IDLE
        
    def output(self):
        if self._cur_state == SimulationModelState.PROCESS:
            #TODO refer DB, Create Docker Container
            self.cal_health()
            print(self.cur_state_level)
            
            # 시뮬레이션 종료
            if self.cur_state_level == self.human_info["state"]:
                print("simulation finished")
                
                self.result_data["human_id"]= self.human_info["human_id"]
                self.result_data["simulated_id"]= self.human_info["simulated_id"]
                self.result_data["log"]= self.simulation_log
                self.result_data["result_health"]= self.simulation_log[self.cur_state_level - 1]["simulated_health"]
                self.result_data["result_prediction"]= self.simulation_log[self.cur_state_level - 1]["prediction"]
                
                print(self.result_data)
                
                self.dealer.send_string(json.dumps(self.result_data))
            
            # 단계 증가
            self.cur_state_level += 1
            
            
        elif self._cur_state == SimulationModelState.IDLE:
            print(SimulationModelState.IDLE)
                

    
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
        log = {}
        
        source_site= self.human_info["site_id"]
        target_site= random.randint(1, 5)
        
        origin_health= round(self.human_info["health"], 3)
        
        
                
        # cur_site에 따른 변화 필요 met = pose 로 간주함
        workIntensity, wbgt, smock, met, noise, site_open, site_cowork = self.num_converter(target_site)
        
        
        # 남자
        if self.human_info["gender"] == 0 :
            # 당뇨병
            if self.human_info["disease"] == ChronicDisease.DIABETES_MELLITUS.value and workIntensity == 4:
                self.human_info["health"] -= 0.9*smock + 1*met*1.2 + 1.1*wbgt
                
            # 고혈압
            elif self.human_info["disease"] == ChronicDisease.HYPERTENSION.value and workIntensity == 5:
                self.human_info["health"] -= 0.9*smock + 1*met*1.3 + 1.1*wbgt*1.1
            
            # 난청
            elif self.human_info["disease"] == ChronicDisease.HYPACUSIS.value and target_site == 5:
                self.human_info["health"] -= (0.9*smock + 1*met + 1.1*wbgt)*1.2

            # 열중증
            elif self.human_info["disease"] == ChronicDisease.HYPERTHERMIA.value and wbgt == 5:
                self.human_info["health"] -= 0.9*smock + 1*met + 1.1*wbgt*1.3
            
            # 관절염
            elif self.human_info["disease"] == ChronicDisease.ARTHRITIS.value and met == 2:
                self.human_info["health"] -= (0.9*smock + 1*met + 1.1*wbgt)*1.1
            
            # Default
            else :
                self.human_info["health"] -= 0.9*smock + 1*met + 1.1*wbgt
        
        # 여자
        else :
            self.human_info["health"] -= 1.1*smock + 1.2*met + 1.3*wbgt
            
            if self.human_info["disease"] == ChronicDisease.DIABETES_MELLITUS.value and workIntensity == 4:
                self.human_info["health"] -= 1.1*smock + 1.2*met*1.2 + 1.3*wbgt
                
            elif self.human_info["disease"] == ChronicDisease.HYPERTENSION.value and workIntensity == 5:
                self.human_info["health"] -= 1.1*smock + 1.2*met*1.3 + 1.3*wbgt*1.1
                
            elif self.human_info["disease"] == ChronicDisease.HYPACUSIS.value and target_site == 5:
                self.human_info["health"] -= (1.1*smock + 1.2*met + 1.3*wbgt)*1.2
            
            elif self.human_info["disease"] == ChronicDisease.HYPERTHERMIA.value and wbgt == 5:
                self.human_info["health"] -= 1.1*smock + 1.2*met + 1.3*wbgt*1.3
                
            elif self.human_info["disease"] == ChronicDisease.ARTHRITIS.value and met == 2:
                self.human_info["health"] -= (1.1*smock + 1.2*met + 1.3*wbgt)*1.1
                
            else :
                self.human_info["health"] -= 1.1*smock + 1.2*met + 1.3*wbgt
            
        prediction = self.classifier(self.human_info["health"], site_open, site_cowork)
        
        log["state"]= self.cur_state_level
        log["source_site"]= source_site
        log["target_site"]= target_site
        log["moving_speed"]= random.randint(1, 3)
        log["origin_health"]= origin_health
        log["simulated_health"]= round(self.human_info["health"], 3)
        log["prediction"]= prediction
        
        # Check Log
        print(log)
        
        self.simulation_log.append(log)
        
        self.human_info["site_id"]= target_site
    
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
    
    def zmq_init(self):
        context= zmq.Context()
        dealer= context.socket(zmq.DEALER)
        dealer.connect(f"tcp://{ContainerConfig.host}:{ContainerConfig.port}")
        
        return dealer
    