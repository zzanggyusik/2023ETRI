from base.execution_engine import ExecutionEngine
from human_agent import HumanAgent
from site_agent import SiteAgent
import time
from multiprocessing import Pool
from rx import create
import zmq

from human_boot_loader import HumanBootLoader
from stand_parts_model import StandPartsModel
from sit_parts_model import SitPartsModel

class Executor():
    def __init__(self) -> None:
        self.parts_list = ["sit_parts_model.simx", "stand_parts_model.simx"]
        self.simulation_number = 50
        self.zmq_init()

    def run(self):
        self.set_agent()
        self.set_parts_model()
        self.set_bootloader()
        self.set_engine()
        
        # Start Simulation
        start_time = time.time()
        for i in range(self.simulation_number) : 
            self.engine.run_multi_parts()
            
        end_time = time.time()
        execution_time = end_time - start_time
        print("병렬 실행 시간: {}초".format(execution_time))
        
    def set_agent(self) -> None:
        """
        Agent 등록
        """
        self.human = HumanAgent("hg", 1, 2, 3, 100, 1, 0)
        self.site = SiteAgent("site1", 1000)
            
    def set_parts_model(self) -> None:
        """
        Parts Model 빌드
        """
        StandPartsModel(self.simulation_number).build_parts_model()
        SitPartsModel(self.simulation_number).build_parts_model()        
        
    def set_bootloader(self) -> None:
        """
        Boot Loader 빌드
        """
        HumanBootLoader(self.parts_list).build_bootloader()

    def set_engine(self) -> None:
        """
        Execution Engine 설정
        """
        # Human 모델에 붙을 Parts model 수
        self.engine = ExecutionEngine(len(self.parts_list))
        
        # Boot Loader 등록
        self.engine.append_bootloader("SIMULATE", "./bootloader/human_boot_loader.simx")

        self.engine.state = "SIMULATE"
        
        # Agent Rx 설정(구독)
        self.engine.set_agent_source(self.human.get_source())
        self.engine.set_env_source(self.site.get_source())

        # Boot Loader 실행, Parts Model 연동
        self.engine.run_boot_loader()
        
    def zmq_init(self) -> None:
        context = zmq.Context()
        self.subscriber = context.socket(zmq.SUB)
        sub_url = f"tcp://MasterNodeName:5555"
        self.subscriber.connect(sub_url)
        self.subscriber.setsockopt_string(zmq.SUBSCRIBE, "TOPIC(human_id)")
        print(f"Subscribe at {sub_url}")
        
        
if __name__ == "__main__":
    Executor().run()

    
    