from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from worker_model import HumanModel
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
        
        worker_model = HumanModel(0, Infinite, Init.modle_manager_name, Init.ename, self.agent_engine)
        
        self.agent_engine.register_entity(worker_model)
        
        self.agent_engine.coupling_relation(None, SimulationConfig.workerModel_start, worker_model, SimulationConfig.workerModel_start)

    def get_engine(self):
        return self.agent_engine
        
    def start_engine(self) -> None:
        self.agent_engine.insert_external_event(SimulationConfig.workerModel_start, SimulationConfig.workerModel_start)
        self.agent_engine.simulate()