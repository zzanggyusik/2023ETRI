from instance.config import *
from enum import Enum

class Init():
    ename = 'Agentsim'
    simulation_time = 'VIRTUAL_TIME'
    simulation_uint_time = 1
    
    modle_manager_name = 'model_manager'

class SimulationConfig():
    workerModel_start = 'worker_start'
    workerModel_finish = 'worker_finish'
    IDLE = 'IDLE'
    
class AgentContainerConfig():
    image_name= "bodlehg/pyrexiasim:agent"
    get_container_name= "CONTAINER_NAME"
    get_port="PORT"
    
class MongoDBConfig():
    host= MONGODB_IP # 1
    port= MONGODB_PORT

    host_url = HOST_URL
    
class SimulationModelState():
    IDLE = "IDLE"
    PROCESS = "PROCESS"
    FINISH = 'FINISH'
    
class ContainerConfig():
    host= "host.docker.internal"
    port= 9999
    container_name = 'CONTAINER_NAME'

class Smock(Enum):
    VERY_LIGHT= 1.0
    LIGHT= 1.1
    MEDIUM= 1.2
    HEAVY= 2.5
    VERY_HEAVY= 4
    
class Pose(Enum):
    STANDING= 1
    SITTING= 2

class Noise(Enum):
    SILENT= 1
    QUIET= 2
    MODERATE= 3
    NOISY= 4
    LOUD= 5
    
class Temperture(Enum):
    SUITABLE= 1.0
    MILD= 1.1
    WARM= 1.2
    # COOL= 3
    HOT= 2.5
    # COLD= 4
    SCORCHING= 3.5
    # FREEZEING= 5
    
class Site(Enum):
    OPEN_SPACE= 0
    CLOSE_SPACE= 1
    COOPERATION= 2
    INDEPENDENT= 3
    
class WorkIntensity(Enum):
    EASY= 1
    MANAGEABLE= 2
    MODERATE= 3
    CHALLENGING= 4
    DIFFICULT= 5

class ChronicDisease(Enum):
    # 관절염
    ARTHRITIS= 1
    # 고혈압
    HYPERTENSION= 2
    # 난청
    HYPACUSIS= 3
    # 열중증
    HYPERTHERMIA= 4
    # 당뇨병
    DIABETES_MELLITUS= 5
    
class Classifier():
    DANGEROUS = 'Dangerous'
    WARNING = 'Warning'
    GOOD = 'Good'
    
