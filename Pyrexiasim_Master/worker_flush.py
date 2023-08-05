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

            key, value = data
            if key in self.log_map:
                self.log_map[key].append(value)
            else:
                self.log_map[key] = [value]
                
        elif port == WorkerFlushConfig.flush_port:
            data = msg.retrieve()[0]
            with open(f"{data['human_id']}.log", "w") as f:
                f.writelines(self.log_map[data['human_id']])
                del self.log_map[data['human_id']]
    
    def output(self):
        pass

    def int_trans(self):
        if self._cur_state == WorkerFlushConfig.IDLE:
            self._cur_state = WorkerFlushConfig.IDLE