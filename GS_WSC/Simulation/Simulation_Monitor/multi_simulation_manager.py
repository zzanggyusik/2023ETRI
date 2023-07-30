from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from monitoring_model import MonitoringModel
import json

class SimMonitor():
    def __init__(self):        
        # initialize simulation engine
        # System Simulator Initialization
        self.ss = SystemSimulator()
        with open("./_instance/multi_config.json") as config_file:
            self.config = json.load(config_file)
        #-----------------------------------------------------------------------
        engine_config = self.config["Engine_config"]
        self.ss.register_engine(engine_config["engine_name"], engine_config["simulation_time"], engine_config["simulation_time_unit"])
        # self.ss.register_engine("monitoring_engine", "REAL_TIME / VIRTUAL_TIME", 1)
        
        self.monitoring_engine = self.ss.get_engine(engine_config["engine_name"])
        
        self.monitoring_engine.insert_input_port("monitoring_start")
        self.monitoring_engine.insert_input_port("IDLE")
        self.monitoring_engine.insert_input_port("monitoring_finish")
        
        model_config = self.config["Model_config"]
        monitoring_model = MonitoringModel(0, Infinite, model_config["model_name"], engine_config["engine_name"], self.monitoring_engine, self.config)
        
        self.monitoring_engine.register_entity(monitoring_model)
        
        self.monitoring_engine.coupling_relation(None, "monitor_start", monitoring_model, "monitor_start")
        #self.monitoring_engine.coupling_relation(monitoring_model, "IDLE", monitoring_model, "monitor_finish")

    def get_engine(self):
        return self.monitoring_engine
        
    def start_engine(self) -> None:
        # if model == "predict":
        self.monitoring_engine.insert_external_event("monitoring_start", "monitoring_start")
        # self.ai_engine.insert_external_event("predict", "predict")
        self.monitoring_engine.simulate()