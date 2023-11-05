from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from worker_model import HumanModel
import os
from instance.config import *
import json

class Agentsim():
    def __init__(self):        
        # initialize simulation engine
        # System Simulator Initialization
        self.ss = SystemSimulator()
        
        self.ss.register_engine(Init.ename, "REAL_TIME", Init.simulation_uint_time)
        
        self.agent_engine = self.ss.get_engine(Init.ename)
        
        self.agent_engine.insert_input_port(SimulationConfig.workerModel_start)
        self.agent_engine.insert_input_port(SimulationConfig.IDLE)
        
        # Get Container name - Human Info
        self.cur_container_name = os.getenv(ContainerConfig.container_name).split('_')
        # Test Code
        # self.cur_container_name = 'containertestingcode_1_8_2_77_0_3_177_78'.split('_')
        # Preprocessing Human Info
        self.human_info = {}
        
        self.human_info["human_id"]= self.cur_container_name[0]
        self.human_info["simulated_id"]= self.cur_container_name[0] + "_" + self.cur_container_name[1]
        self.human_info["state"] = float(self.cur_container_name[2])
        self.human_info["site_id"] = float(self.cur_container_name[3])
        self.human_info["health"] = float(self.cur_container_name[4])
        self.human_info["gender"] = float(self.cur_container_name[5])
        self.human_info["disease"] = float(self.cur_container_name[6])
        self.human_info["height"] = float(self.cur_container_name[7])
        self.human_info["weight"] = float(self.cur_container_name[8])        
        
        # Register Entity -> Simulation while state
        worker_model = HumanModel(0, self.human_info["state"] + 1, Init.modle_manager_name, Init.ename, self.agent_engine, self.human_info)
        
        self.agent_engine.register_entity(worker_model)
        
        self.agent_engine.coupling_relation(None, SimulationConfig.workerModel_start, worker_model, SimulationConfig.workerModel_start)

    def get_engine(self):
        return self.agent_engine
        
    def start_engine(self) -> None:
        self.agent_engine.insert_external_event(SimulationConfig.workerModel_start, SimulationConfig.workerModel_start)
        self.agent_engine.simulate()