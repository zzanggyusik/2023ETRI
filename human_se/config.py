from enum import Enum

class SimulationPort():
    humanInfoModel_start = "humanInfoModel_start"
    humanInfoModel_finish = "humanInfoModel_finish"
    
    humanSimulation_start = "humanSimulation_start"
    humanSimulation_finish = ""
    #####################################################
    partsModelHandler_start = "partsModelHandler_start"
    partsModelHandler_finish = "partsModelHandler_finish"

    partsModel_start = "partsModel_start"
    partsModel_finish = "partsModel_finish"
    
    # partsModel_start = "partsModel_start"
    # partsModel_finish = "partsModel_finish"
    
    
    
    
class SimulationModelState():
    IDLE = "IDLE"
    PROCESS = "PROCESS"
    FINISH = "FINISH"
     
class PartsModelPubPorts(Enum):
    sit = 5555
    stand = 5556


    