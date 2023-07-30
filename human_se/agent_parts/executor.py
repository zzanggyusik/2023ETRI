from base.execution_engine import ExecutionEngine
from human_agent import HumanAgent
from site_agent import SiteAgent
import time
from multiprocessing import Pool
from rx import create
from human_boot_loader import HumanBootLoader
from stand_parts_model import StandPartsModel
from sit_parts_model import SitPartsModel

if __name__ == "__main__":
    parts_list = ["sit_parts_model.simx", "stand_parts_model.simx"]    
    simulation_number = 50
    
    human = HumanAgent("hg", 1, 2, 3, 100, 1, 0)
    site = SiteAgent("site1", 1000)
    
    
    StandPartsModel(simulation_number).build_parts_model()
    SitPartsModel(simulation_number).build_parts_model()
    HumanBootLoader(parts_list).build_bootloader()
    
    # Human 모델에 붙을 Parts model 수
    engine = ExecutionEngine(len(parts_list))
    
    engine.append_bootloader("SIMULATE", "./bootloader/human_boot_loader.simx")

    engine.state = "SIMULATE"
    engine.set_agent_source(human.get_source())
    engine.set_env_source(site.get_source())

    engine.run_boot_loader()
    
    #병렬 실행 적용
    start_time = time.time()
    for i in range(simulation_number) : 
        engine.run_multi_parts()
        
    
    end_time = time.time()
    execution_time = end_time - start_time
    print("병렬 실행 시간: {}초".format(execution_time))
    
    