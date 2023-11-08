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
    
class MonitorModelConfig():
    # Model Name
    model_name= "monitor_model"
    
    # Model State
    IDLE= "IDLE"
    PROCESSING= "monitoring"
    
    # Monitor Model Port
    monitor_start= "monitor_start"
    monitor_fin= "monitor_finish"
    
class ContainerGeneratorConfig():
    # Model Name
    model_name= "human_id"
    
    # Model State
    IDLE= "IDLE"
    PROCESSING= "processing"    
    
    # Container Generator Model Port
    generator_start= "generator_start"
    generator_fin= "generator_fin"    
    
    
# class ContainerGeneratorConfig():
#     image_name= "bodlehg/pyrexiasim:generator"
#     get_container_name= "CONTAINER_NAME"
    
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
    
    
    
    
    