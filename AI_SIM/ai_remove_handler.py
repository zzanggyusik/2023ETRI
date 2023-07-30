from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.system_executor import SysExecutor
from pyevsim.definition import Infinite
from datetime import datetime

import pymongo

class HumanRemoveModel(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, mname, ename, _engine:SysExecutor, \
                 config):
        super().__init__(inst_t, dest_t, mname, ename)

        # State
        self.init_state("IDLE")        
        self.insert_state("IDLE", Infinite)
        self.insert_state("REMOVE", 0)

        self.insert_input_port("model_name")

        # Domain Part
        self.engine = _engine
        self.config = config

        self.model_list = []

    def ext_trans(self, port, msg):
        if port == "model_name":
            self.model_list.append(msg.retrieve()[0])
            self._cur_state = "REMOVE"    
        pass
   
    def output(self):
        for item in self.model_list:
            self.engine.remove_entity(item)
        self.model_list = []

    def int_trans(self):
        if self._cur_state == "REMOVE":
            self._cur_state = "IDLE"
        pass



