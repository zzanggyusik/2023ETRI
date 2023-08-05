from base.execution_engine import ExecutionEngine
from human_agent import HumanAgent
from site_agent import SiteAgent
import time
from multiprocessing import Pool
from rx import create
import zmq
import json
import sys
from human_boot_loader import HumanBootLoader
from stand_parts_model import StandPartsModel
from sit_parts_model import SitPartsModel

class Executor():
    # def __init__(self, human_info, site_info, parts_list, simulation_number) -> None:
    def __init__(self) -> None:
        self.container_id = ""
        self.human_info = {}
        self.site_info = {}
        
        self.parts_list = []
        self.simulation_number = 0
        self.zmq_init()

    def run(self):
        try:
            while True:
                print("Receive Ready...")
                json_data = json.loads(self.subscriber.recv_json())
                
                self.set_init(json_data)                
                
                # Agent 등록
                self.set_agent()
                # Parts Model 등록
                self.set_parts_model()
                # BootLoader를 통해 Parts Model 연동
                self.set_bootloader()
                self.set_engine()
                
                # Start Simulation
                start_time = time.time()
                for i in range(self.simulation_number) : 
                    self.engine.run_multi_parts()
                    
                end_time = time.time()
                execution_time = end_time - start_time
                print("병렬 실행 시간: {}초".format(execution_time))
        except KeyboardInterrupt:
            print("Service Terminated")
    
    def set_init(self, json_data) -> None:
        self.container_id = json_data["container_id"]
        self.human_info = json_data["human_info"]
        self.site_info = json_data["site_info"]
        
        self.parts_list = json_data["parts_list"]
        self.simulation_number = json_data["simulation_number"]
    
    def set_agent(self) -> None:
        """
        Agent 등록
        """
        
        self.human = HumanAgent(self.human_info)
        self.site = SiteAgent(self.site_info)
            
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
        sub_url = f"tcp://MasterNode:5555"
        self.subscriber.connect(sub_url)
        self.subscriber.setsockopt_string(zmq.SUBSCRIBE, "TOPIC(human_id)")
        print(f"Subscribe at {sub_url}")
        
        
if __name__ == "__main__":
    
    Executor().run()
    
    # argv Set
    # No argv
    # if len(sys.argv) == 1:
    #     # Default For Test
    #     human_info = {"id": "hg", "smock": 1, \
    #                         "wbgt": 2, "met": 3, \
    #                             "health": 100, "out": 1, \
    #                                 "simulation_number": 0}
    #     site_info = {"name": "site1", "site": 1000}           
    #     parts_list = ["sit_parts_model.simx", "stand_parts_model.simx"]
    #     simulation_number = 50      
        
    #     Executor(human_info, site_info, parts_list, simulation_number).run()
        
    # elif len(sys.argv) > 1:
        
    #     # Get Argument
    #     human_info = sys.argv[1]
    #     site_info = sys.argv[2]
    #     parts_list = sys.argv[3]
    #     simulation_number = sys.argv[4]
    #     Executor(human_info, site_info, parts_list, simulation_number).run()

    
    