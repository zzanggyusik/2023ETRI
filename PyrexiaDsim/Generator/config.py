class PyrexiaDsimConfig():
    # PATH
    path= "./Simulation/simulation.py"
    result_path= "./Result/"
    
    # Engine Setting
    mode= "REAL_TIME",
    # mode= "VIRTUAL_TIME",
    time_step= 1
    instance_number= 100
    
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
    
class ContainerGeneratorConfig():
    image_name= "bodlehg/pyrexiasim:generator"
    get_container_name= "CONTAINER_NAME"
    
class AgentContainerConfig():
    image_name= "bodlehg/pyrexiasim:agent"
    get_container_name= "CONTAINER_NAME"
    
class MongoDBConfig():
    host= "192.168.50.201" # 1
    # host= "121.152.137.202" # 2
    port= 27017
    
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
    
        
    
    
    