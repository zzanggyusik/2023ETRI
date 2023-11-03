from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from PyrexiaDsim.monitor_model import HumanModel
import json

class PyrexiaDsim():
    def __init__(self):        
        # initialize simulation engine
        # System Simulator Initialization
        self.ss = SystemSimulator()
        with open("./_instance/config.json") as config_file:
            self.config = json.load(config_file)
        #-----------------------------------------------------------------------
        engine_config = self.config["Simulation_config"]["engine_config"]
        model_config = self.config["Simulation_config"]["model_config"]
        
        self.ss.register_engine(engine_config["engine_name"], engine_config["simulation_time"], engine_config["simulation_time_unit"])
        # self.ss.register_engine("monitoring_engine", "REAL_TIME / VIRTUAL_TIME", 1)
        
        self.controller_engine = self.ss.get_engine(engine_config["engine_name"])
        
        self.controller_engine.insert_input_port("monitor_start")
        self.controller_engine.insert_input_port("IDLE")
        
        controller_model = HumanModel(0, Infinite, model_config["model_name"], engine_config["engine_name"], self.controller_engine, self.config)
        
        self.controller_engine.register_entity(controller_model)
        
        self.controller_engine.coupling_relation(None, "monitor_start", controller_model, "monitor_start")

    def get_engine(self):
        return self.controller_engine
        
    def start_engine(self) -> None:
        self.controller_engine.insert_external_event("monitor_start", "monitor_start")
        self.controller_engine.simulate()