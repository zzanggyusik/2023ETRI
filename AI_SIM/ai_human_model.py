from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.system_message import SysMessage
from pyevsim.system_executor import SysExecutor
from pyevsim.definition import Infinite
from datetime import datetime

import pymongo

class HumanModel(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, mname, ename, _engine:SysExecutor, \
                 config, db_config):
        super().__init__(inst_t, dest_t, mname, ename)

        self.db_url = f"mongodb://{db_config['site_human_db']['db_user']}:{db_config['site_human_db']['db_pw']}@{db_config['site_human_db']['db_addr']}"
        self.db = pymongo.MongoClient(self.db_url)[db_config['site_human_db']['db_name']]
        
        self.collection_name = f"{db_config['site_human_db']['db_collection_name']}"

        # State
        self.init_state("RUN")
        self.insert_state("RUN", 1)
        self.insert_state("SEND", 0)
        self.insert_state("IDLE", Infinite)

        self.insert_output_port("out")

        # Domain Part
        self.engine = _engine
        self.config = config
        self.index = 0
        self.next_time = self.config[self.index][2]

        print("@@@")

    def ext_trans(self, port, msg):
        pass
   
    def output(self):
        if self._cur_state == "RUN":
            
            gt = self.engine.get_global_time()
            print(f"{self.get_name()}:{gt}, {self.next_time}")

            if self.index < len(self.config):
                data = {'timestamp':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),\
                        'human_id': f"{self.get_name()}", 'smock': self.config[self.index][0],\
                        'work_intensive': self.config[self.index][1]}
                print(data)
                self.db[self.collection_name].update_one({'human_id':f'{data["human_id"]}'}, {'$set':data},upsert=True)

            if gt > self.next_time:
                self.index += 1
            
                if self.index < len(self.config):
                    self.next_time = gt + self.config[self.index][2]
                
                print(self.index)

        elif self._cur_state == "SEND":
            msg = SysMessage(self.get_name(), "out")
            msg.insert(self.get_name())
            return msg
    
    def int_trans(self):
        if self._cur_state == "RUN":
            self._cur_state = "RUN"
        elif self._cur_state == "SEND":
            self._cur_state = "IDLE"
        
        if self._cur_state == "RUN" and self.index >= len(self.config):
            self._cur_state = "SEND"

        pass



