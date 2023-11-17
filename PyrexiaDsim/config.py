from instance.config import *

class PyrexiaDsimConfig():
    # PATH
    path= "./Simulation/simulation.py"
    result_path= "./Result/"
    
    # Engine Setting
    mode= "REAL_TIME",
    # mode= "VIRTUAL_TIME",
    time_step= 1
    # instance_number= 100
    instance_number= 20
    
    engine_name= "pyrexiadsim_engine"
    model_name= "monitor_model"
    
    ## Simulation Engine Input Port
    monitor_start= "monitor_start"
    IDLE= "IDLE"
    
    max_worked_time= 8
    
class MonitorModelConfig():
    # Model Name
    model_name= "monitor_model"
    
    # Model State
    IDLE= "IDLE"
    PROCESSING= "monitoring"
    
    # Model Port
    start= "monitor_start"
    fin= "monitor_finish"
    model_in= "monitor_in"
    
class ContainerGeneratorConfig():
    # image_name= "bodlehg/pyrexiasim:generator"
    # get_container_name= "CONTAINER_NAME"
    
    IDLE= "IDLE"
    PROCESSING= "monitoring"
    start= "generator_start"
    fin= "generator_finish"    
    
    out= "generator_out"
    
    
    
class AgentContainerConfig():
    # image_name= "zzanggyusik/pyrexiasim:agent"
    image_name= "bodlehg/pyrexiasim:agent"
    get_container_name= "CONTAINER_NAME"
    
class MongoDBConfig():
    host= MONGODB_IP # 2
    port= MONGODB_PORT

    host_url = HOST_URL
    
class ZMQ_NetworkConfig():
    """
    Network Config between monitor_model and container_generator,
    between container_generator and human_agent container. 
    r: ROUTER, d: DEALER
    """
    
    # Network Config between monitor_model and container_generator
    monitor_r_host= "*"
    monitor_r_port= 8888
    
    generator_d_host= "host.docker.internal"
    generator_d_port= 8888
    
    # Network Config between container_generator and human_agent container
    generator_r_host= "*"
    generator_r_port= 9999
    
    agent_d_host= "host.docker.internal"
    agent_d_port= 9999


# Parts Magic Number

from enum import Enum

class Gender(Enum):
    MALE= 0
    FEMALE= 1

class Smock(Enum):
    VERY_LIGHT= 1
    LIGHT= 2
    MEDIUM= 3
    HEAVY= 4
    VERY_HEAVY= 5
    
    
class SiteID(Enum):
    VISION1= 0
    VISION2= 1
    VISION3= 2
    VISION4= 3
    VISION5= 4
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
    SUITABLE= 1
    MILD= 2
    WARM= 3
    # COOL= 3
    HOT= 4
    # COLD= 4
    SCORCHING= 5
    # FREEZEING= 5
    
class SiteFeature(Enum):
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

class Gender(Enum):
    MALE= 0
    FEMALE= 1

class ChronicDisease(Enum):
    # 관절염
    ARTHRITIS= 0
    # 고혈압
    HYPERTENSION= 1
    # 난청
    HYPACUSIS= 2
    # 열중증
    HYPERTHERMIA= 3
    # 당뇨병
    DIABETES_MELLITUS= 4
    
        
    
    
    
