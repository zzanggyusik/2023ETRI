from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from Agent.worker_model import HumanModel
from instance.config import *
import json

class Agentsim():
    def __init__(self):        
        # initialize simulation engine
        # System Simulator Initialization
        self.ss = SystemSimulator()
        
        self.ss.register_engine(Init.ename, Init.simulation_time, Init.simulation_uint_time)
        
        self.agent_engine = self.ss.get_engine(Init.ename)
        
        self.agent_engine.insert_input_port(SimulationConfig.workerModel_start)
        self.agent_engine.insert_input_port(SimulationConfig.IDLE)
        
        controller_model = HumanModel(0, Infinite, Init.modle_manager_name, Init.ename, self.agent_engine)
        
        self.agent_engine.register_entity(controller_model)
        
        self.agent_engine.coupling_relation(None, "monitor_start", controller_model, "monitor_start")

    def get_engine(self):
        return self.agent_engine
        
    def start_engine(self) -> None:
        self.agent_engine.insert_external_event("monitor_start", "monitor_start")
        self.agent_engine.simulate()