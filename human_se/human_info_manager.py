from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from human_info_model import HumanInfoModel
from human_parts_manager_model import HumanPartsManagerModel
from config import SimulationPort
# from scenario_model import ScenarioModel
# from mobilenet_model import MobileNetModel
# from cnn_model import CNNModel
# from traffic_sign_model import TrafficSignModel

# import zmq
import threading
from data_object import DataObject

class HumanInfoManager():
    def __init__(self):
                
        # initialize simulation engine
        # System Simulator Initialization
        self.ss = SystemSimulator()
        #-----------------------------------------------------------------------
        # self.ss.register_engine("AIModelVerifier", "REAL_TIME", 1)
        self.ss.register_engine("HumanSimulator", "VIRTUAL_TIME", 1)
        # self.ss.register_engine("motorcontrol", "REAL_TIME", 1)
        
        self.human_engine = self.ss.get_engine("HumanSimulator")
        # self.control_engine = self.ss.get_engine("motorcontrol")
        self.human_engine.insert_input_port(SimulationPort.humanInfoModel_start)
        self.human_engine.insert_input_port(SimulationPort.humanInfoModel_finish)
        
        self.human_engine.insert_input_port(SimulationPort.humanSimulation_start)
        
        # self.data_object = DataObject()
        
        human_info_model = HumanInfoModel(instance_time = 0, destruct_time = Infinite, \
                                          name = "Human Info Model", engine_name = "HumanSimulator", \
                                            engine = self.human_engine)
        human_parts_manager_model = HumanPartsManagerModel(instance_time = 0, destruct_time = Infinite, \
                                          name = "Human Parts Manager Model", engine_name = "HumanSimulator", \
                                            engine = self.human_engine)
        
        # cnn_model = CNNModel(0, Infinite, "cnn", "AIModelVerifier", self.human_engine, self.data_object)
        # traffic_sign_model = TrafficSignModel(0, Infinite, "TrafficSignModel", "AIModelVerifier", self.human_engine, self.data_object)
        
        self.human_engine.register_entity(human_info_model)
        self.human_engine.register_entity(human_parts_manager_model)
        # self.human_engine.register_entity(cnn_model)
        # self.human_engine.register_entity(traffic_sign_model)
        
        self.human_engine.coupling_relation(None, SimulationPort.humanInfoModel_start, \
                                        human_info_model, SimulationPort.humanInfoModel_start)
        self.human_engine.coupling_relation(human_info_model, "process", \
                                        human_parts_manager_model, "aimodel_start")
        
        # self.human_engine.coupling_relation(scenario_model, "process", mobilenet_model, "aimodel_start")
        # self.human_engine.coupling_relation(scenario_model, "process", traffic_sign_model, "aimodel_start")
        # self.human_engine.coupling_relation(traffic_sign_model, "process", scenario_model, "scenario_start")
        # self.human_engine.coupling_relation(cnn_model, "process", scenario_model, "scenario_start")

        
    def get_engine(self):
        return self.human_engine
        
    def start_engine(self) -> None:
        # if model == "predict":
        self.human_engine.insert_external_event(SimulationPort.humanInfoModel_start, SimulationPort.humanInfoModel_start)
        # self.human_engine.insert_external_event("predict", "predict")
        self.human_engine.simulate()
        
            
        
            

            
        

  

  
        
    

        

