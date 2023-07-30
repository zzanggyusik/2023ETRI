from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from human_model import HumanModel
import json

class Human():
    def __init__(self):        
        # initialize simulation engine
        # System Simulator Initialization
        self.ss = SystemSimulator()
        with open("./_instance/human_config.json") as config_file:
            self.config = json.load(config_file)
        #-----------------------------------------------------------------------
        engine_config = self.config["Simulation_config"]["engine_config"]
        model_config = self.config["Simulation_config"]["model_config"]
        
        self.ss.register_engine(engine_config["engine_name"], engine_config["simulation_time"], engine_config["simulation_time_unit"])
        # self.ss.register_engine("monitoring_engine", "REAL_TIME / VIRTUAL_TIME", 1)
        
        self.controller_engine = self.ss.get_engine(engine_config["engine_name"])
        
        self.controller_engine.insert_input_port("human_model_start")
        self.controller_engine.insert_input_port("IDLE")
        self.controller_engine.insert_input_port("human_model_finish")
        
        controller_model = HumanModel(0, Infinite, model_config["model_name"], engine_config["engine_name"], self.controller_engine, self.config)
        
        self.controller_engine.register_entity(controller_model)
        
        self.controller_engine.coupling_relation(None, "human_model_start", controller_model, "human_model_start")
        #self.monitoring_engine.coupling_relation(monitoring_model, "IDLE", monitoring_model, "monitor_finish")

    def get_engine(self):
        return self.controller_engine
        
    def start_engine(self) -> None:
        # if model == "predict":
        self.controller_engine.insert_external_event("human_model_start", "human_model_start")
        # self.ai_engine.insert_external_event("predict", "predict")
        self.controller_engine.simulate()