from base.execution_engine import ExecutionEngine
from human_agent import HumanAgent
from site_agent import SiteAgent
import time
from datetime import datetime
from multiprocessing import Pool
from rx import create
import os, sys
import zmq
import json
import sys
from human_boot_loader import HumanBootLoader
from stand_parts_model import StandPartsModel
from sit_parts_model import SitPartsModel
from pymongo import MongoClient
from config import *

class Executor():
    # def __init__(self, human_info, site_info, parts_list, simulation_number) -> None:
    def __init__(self) -> None:
        self.container_name = "container1"
        self.human_info = {"id": "person1", "smock": 1, \
                            "wbgt": 2, "met": 3, \
                                "exist": 0, "hp": 0}
        
        self.site_info = {"name": "site1", "site": 1000}   
        
        # self.container_name = os.getenv("CONTAINER_NAME")
        
        self.parts_list = ["sit_parts_model.simx", "stand_parts_model.simx"]
        self.simulation_number = 50
        self.seed = 34
        
        #self.mongo_client = MongoClient(host= "192.168.50.113", port= 27017) # Local
        self.mongo_client = MongoClient(host= MONGODB_HOST, port= MONGODB_PORT) # Docker
        
        self.context = zmq.Context()
        self.zmq_dealer_init()
        self.zmq_sub_init()

        self.dealer.send_string(str(self.container_name))
        
    def run(self):
        try:
            while True:
                print("Receive Ready...")
                topic, json_data = self.demogrify(self.subscriber.recv_string())
                
                self.set_human_info(json_data)
                
                # self.set_init(json_data)                
                
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
                
                self.update_db()
                
                data = {
                    "client_name" : self.container_name,
                    "message" : "Task Done"
                }
                
                self.dealer.send_string(json.dumps(data))
                print(f'Work Finish {data}')
                
                break
                # print(f"시뮬레이션 결과 : {self.human.agent}")
                # print("병렬 실행 시간: {}초".format(execution_time))
        except KeyboardInterrupt:
            print("Service Terminated")
    
    def set_init(self, json_data) -> None:
        # self.container_id = json_data["container_id"]
        self.human_info = json_data["human_info"]
        self.site_info = json_data["site_info"]
        
        self.parts_list = json_data["parts_list"]
        self.simulation_number = json_data["simulation_number"]
        
        self.human_db = self.mongo_client[self.human_info['id']]
        
    def set_human_info(self, json_data) -> None:
        self.human_info = json_data
        print(self.human_info)
    
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
        StandPartsModel().build_parts_model()
        SitPartsModel().build_parts_model()        
        
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
        
    def update_db(self):
        
        db_name = f"human:{self.human_info['id']}"
        mongo_db = self.mongo_client[db_name]
        
        coll_name = f"{self.container_name}_seed:{self.seed}"
        mongo_coll = mongo_db[coll_name]
        
        self.human.agent["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        mongo_coll.insert_one(self.human.agent)
        
    def zmq_dealer_init(self) -> None:
        """
        Dealer init // to send container state (running / task done)
        """
        self.dealer = self.context.socket(zmq.DEALER)
        self.dealer_url = f'tcp://{DEALER_HOST}:{DEALER_PORT}'
        self.dealer.connect(f'tcp://{DEALER_HOST}:{DEALER_PORT}')
        print(f"Dealer Work at {self.dealer_url}")

    def zmq_sub_init(self) -> None:
        """
        Subscriber Init // 
        """
        self.subscriber = self.context.socket(zmq.SUB)
        sub_url = f"tcp://{SUBSCRIBE_HOST}:{SUBSCRIBE_PORT}"
        self.subscriber.connect(sub_url)
        self.subscriber.setsockopt_string(zmq.SUBSCRIBE, self.human_info["id"])
        print(f"Subscribe at {sub_url}")
        
    def demogrify(self, topicmsg):
        """ Inverse of mogrify() """
        json0 = topicmsg.find('{')
        topic = topicmsg[0:json0].strip()
        msg = json.loads(topicmsg[json0:])
        return topic, msg
        
if __name__ == "__main__":
    Executor().run()

    
    