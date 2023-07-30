from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.system_executor import SysExecutor
from pyevsim.system_simulator import SystemSimulator
from pyevsim.definition import Infinite
from ai_human_model import HumanModel
from ai_remove_handler import HumanRemoveModel

import json

class GeneratorModel(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, mname, ename, _engine:SysExecutor, config):
        super().__init__(inst_t, dest_t, mname, ename)

        with open('./instance/db_config.json') as _file:
            self.db_config = json.load(_file)

        # X
        self.insert_input_port("human_info")

        # State
        self.init_state("WAIT")
        self.insert_state("WAIT", Infinite)
        self.insert_state("GEN", 0)

        # Domain Part
        self.engine = _engine
        self.config = config
        self.human_info_list = []

        self.remove_handler = HumanRemoveModel(0, Infinite, "rm", "seni", self.engine, config)
        self.engine.register_entity(self.remove_handler)
        # Check data
        #self.data = [{'_id': ObjectId('635e53eead92e430f1d7d0b9'),'human_id': '412f6032-aad4-433c-b89c-a9f1755a08ec','smock': 000,'work_intensive': 1}]

    def ext_trans(self, port, msg):
        if port == "human_info":
            print(msg.retrieve()[0])
            self.human_info_list.append(msg.retrieve()[0])
            self._cur_state = "GEN"
        pass
   
    def output(self):
        print(self.human_info_list)
        for lst in self.human_info_list:
            for model in lst:
                model = model.strip()
                hm = HumanModel(0, Infinite, f"{model}", self.get_engine_name(), \
                                self.engine, self.config['human_info'][model], self.db_config)
                self.engine.register_entity(hm)
                self.engine.coupling_relation(hm, "out", self.remove_handler, "model_name")

        self.human_info_list = []
        pass

    def int_trans(self):
        if self._cur_state == "GEN":
            self._cur_state = "WAIT"
        pass



