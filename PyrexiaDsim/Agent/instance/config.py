
class Init():
    ename = 'Agentsim'
    simulation_time = 'VIRTUAL_TIME'
    simulation_uint_time = 1
    
    modle_manager_name = 'model_manager'

class SimulationConfig():
    workerModel_start = 'worker_start'
    workerModel_finish = 'worker_finish'
    IDLE = 'IDLE'
    
class SimulationModelState():
    IDLE = "IDLE"
    PROCESS = "PROCESS"
    FINISH = 'FINISH'
    
class ContainerConfig():
    HOST_PORT = 9999
    container_name = 'CONTAINER_NAME'