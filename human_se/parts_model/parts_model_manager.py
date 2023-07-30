from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from parts_model_pose.parts_model_sit import PartsModelSit
from parts_model_pose.parts_model_stand import PartsModelStand
from parts_model_handler import PartsModelHandler

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import SimulationPort

# from scenario_model import ScenarioModel
# from mobilenet_model import MobileNetModel
# from cnn_model import CNNModel
# from traffic_sign_model import TrafficSignModel

# import zmq
import threading
# from data_object import DataObject

class PartsModelManager():
    def __init__(self):
        
        # initialize simulation engine
        # System Simulator Initialization
        self.ss = SystemSimulator()
        #-----------------------------------------------------------------------
        # self.ss.register_engine("AIModelVerifier", "REAL_TIME", 1)
        self.ss.register_engine("PartsModelSimulator", "VIRTUAL_TIME", 1)
        # self.ss.register_engine("motorcontrol", "REAL_TIME", 1)
        
        self.parts_engine = self.ss.get_engine("PartsModelSimulator")
        # self.control_engine = self.ss.get_engine("motorcontrol")
        
        self.parts_engine.insert_input_port(SimulationPort.partsModelHandler_start)
        self.parts_engine.insert_input_port(SimulationPort.partsModelHandler_finish)
        
        # self.parts_engine.insert_input_port("humansim_start")
        
        # self.data_object = DataObject()
        
        parts_model_handler = PartsModelHandler(instance_time = 0, destruct_time = Infinite, \
                                          name = "Parts Model Handler", engine_name = "PartsModelSimulator", \
                                            engine = self.parts_engine)
        parts_model_sit = PartsModelSit(instance_time = 0, destruct_time = Infinite, \
                                          name = "Parts Model - Sit", engine_name = "PartsModelSimulator", \
                                            engine = self.parts_engine)
        parts_model_stand = PartsModelStand(instance_time = 0, destruct_time = Infinite, \
                                          name = "Parts Model - Stand", engine_name = "PartsModelSimulator", \
                                            engine = self.parts_engine)        
                
        self.parts_engine.register_entity(parts_model_handler)
        self.parts_engine.register_entity(parts_model_sit)
        self.parts_engine.register_entity(parts_model_stand)

        
        # Set Coupling relation
        
        # None -> parts_model_handler
        self.parts_engine.coupling_relation(None, SimulationPort.partsModelHandler_start, \
                                        parts_model_handler, SimulationPort.partsModelHandler_start) 
        # parts_model_handler -> parts_model_sit
        self.parts_engine.coupling_relation(parts_model_handler, SimulationPort.partsModel_start, \
                                        parts_model_sit, SimulationPort.partsModel_start)
        # parts_model_handler -> parts_model_stand
        self.parts_engine.coupling_relation(parts_model_handler, SimulationPort.partsModel_start, \
                                        parts_model_stand, SimulationPort.partsModel_start)        

    def get_engine(self):
        return self.parts_engine
        
    def start_engine(self) -> None:
        # if model == "predict":
        print(SimulationPort.partsModelHandler_start)
        self.parts_engine.insert_external_event(SimulationPort.partsModelHandler_start, SimulationPort.partsModelHandler_start)
        
        self.parts_engine.simulate()
        
            
        
            

            
        

  

  
        
    

        

