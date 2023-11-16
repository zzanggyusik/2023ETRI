from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from monitor_model import MonitorModel
import json
from config import *

class PyrexiaDsim():
    def __init__(self):        
        # initialize simulation engine
        # System Simulator Initialization
        self.ss = SystemSimulator()
        
        self.ss.register_engine(PyrexiaDsimConfig.engine_name, "REAL_TIME", PyrexiaDsimConfig.time_step)
        
        self.pyrexiadsim_engine = self.ss.get_engine(PyrexiaDsimConfig.engine_name)
        
        self.pyrexiadsim_engine.insert_input_port(PyrexiaDsimConfig.monitor_start)
        self.pyrexiadsim_engine.insert_input_port(PyrexiaDsimConfig.IDLE)
        
        monitor_model = MonitorModel(0, Infinite, \
            MonitorModelConfig.model_name, PyrexiaDsimConfig.engine_name, \
                self.pyrexiadsim_engine)
        
        self.pyrexiadsim_engine.register_entity(monitor_model)
        
        self.pyrexiadsim_engine.coupling_relation(None, PyrexiaDsimConfig.monitor_start,\
            monitor_model, PyrexiaDsimConfig.monitor_start)

    def get_engine(self):
        return self.engine
        
    def start_engine(self) -> None:
        self.pyrexiadsim_engine.insert_external_event(PyrexiaDsimConfig.monitor_start, PyrexiaDsimConfig.monitor_start)
        self.pyrexiadsim_engine.simulate()
        
    