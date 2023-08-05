from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.system_simulator import SystemSimulator
from pyevsim.system_message import SysMessage
from pyevsim.definition import *

from config import *

class WorkerFlushModel(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, mname, ename):
        super().__init__(inst_t, dest_t, mname, ename)

        # X
        self.insert_input_port(WorkerFlushConfig.health_info_port)
        self.insert_input_port(WorkerFlushConfig.flush_port)

        self.init_state(WorkerFlushConfig.IDLE)
        self.insert_state(WorkerFlushConfig.IDLE, Infinite)

        self.log_map = {}

    def ext_trans(self, port, msg):
        if port == WorkerFlushConfig.health_info_port:
            data = msg.retrieve()[0]
            # print(f"data = {data.items()}")
            for key, value in data.items():
                pass
            
            # if key in self.log_map.keys():
            #     self.log_map[key] = [value]
            #     # self.log_map[key].append(value)
            # else:
            #     self.log_map[key].append(value)
            self.log_map[key] = [value]
            print(self.log_map)
                
                
        elif port == WorkerFlushConfig.flush_port:
            data = msg.retrieve()[0]
            # print(data)
            # print(self.log_map)
            with open(f"{data['id']}.log", "w") as f:
                print("data: ", str(self.log_map[data['id']]))
                f.writelines(str(self.log_map[data['id']]))
                del self.log_map[data['id']]
    
    def output(self):
        pass

    def int_trans(self):
        if self._cur_state == WorkerFlushConfig.IDLE:
            self._cur_state = WorkerFlushConfig.IDLE