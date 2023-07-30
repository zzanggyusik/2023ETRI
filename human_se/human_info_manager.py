from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from human_info_model import HumanInfoModel
from human_parts_manager_model import HumanPartsManagerModel
# from scenario_model import ScenarioModel
# from mobilenet_model import MobileNetModel
# from cnn_model import CNNModel
# from traffic_sign_model import TrafficSignModel

# import zmq
import threading
from data_object import DataObject

class HumanInfoManager():
    def __init__(self):

        # STATE, EVT = aicar_input_test.main()
        # self.state = state
        # self.evt = evt
        
        # initialize simulation engine
        # System Simulator Initialization
        self.ss = SystemSimulator()
        #-----------------------------------------------------------------------
        # self.ss.register_engine("AIModelVerifier", "REAL_TIME", 1)
        self.ss.register_engine("HumanSimulator", "VIRTUAL_TIME", 1)
        # self.ss.register_engine("motorcontrol", "REAL_TIME", 1)
        
        self.ai_engine = self.ss.get_engine("HumanSimulator")
        # self.control_engine = self.ss.get_engine("motorcontrol")
        
        self.ai_engine.insert_input_port("scenario_start")
        self.ai_engine.insert_input_port("scenario_finish")
        
        self.ai_engine.insert_input_port("humansim_start")
        
        # self.data_object = DataObject()
        
        human_info_model = HumanInfoModel(instance_time = 0, destruct_time = Infinite, \
                                          model_name = "Human Info Model", engine_name = "HumanSimulator", \
                                            engine = self.ai_engine)
        human_parts_manager_model = HumanPartsManagerModel(instance_time = 0, destruct_time = Infinite, \
                                          model_name = "Human Parts Manager Model", engine_name = "HumanSimulator", \
                                            engine = self.ai_engine)
        
        # cnn_model = CNNModel(0, Infinite, "cnn", "AIModelVerifier", self.ai_engine, self.data_object)
        # traffic_sign_model = TrafficSignModel(0, Infinite, "TrafficSignModel", "AIModelVerifier", self.ai_engine, self.data_object)
        
        self.ai_engine.register_entity(human_info_model)
        self.ai_engine.register_entity(human_parts_manager_model)
        # self.ai_engine.register_entity(cnn_model)
        # self.ai_engine.register_entity(traffic_sign_model)
        
        self.ai_engine.coupling_relation(None, "scenario_start", scenario_model, "scenario_start")
        # self.ai_engine.coupling_relation(scenario_model, "process", mobilenet_model, "aimodel_start")
        self.ai_engine.coupling_relation(scenario_model, "process", cnn_model, "aimodel_start")
        self.ai_engine.coupling_relation(scenario_model, "process", traffic_sign_model, "aimodel_start")
        self.ai_engine.coupling_relation(traffic_sign_model, "process", scenario_model, "scenario_start")
        self.ai_engine.coupling_relation(cnn_model, "process", scenario_model, "scenario_start")

        
    def get_engine(self):
        return self.ai_engine
        
    def start_engine(self) -> None:
        # if model == "predict":
        self.ai_engine.insert_external_event("scenario_start", "scenario_start")
        # self.ai_engine.insert_external_event("predict", "predict")
        self.ai_engine.simulate()
        
            
        
            

            
        

  

  
        
    

        

