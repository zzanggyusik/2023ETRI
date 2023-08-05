from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.system_simulator import SystemSimulator
from pyevsim.system_message import SysMessage
from pyevsim.definition import *

from config import *

from typing import TypeVar

ModelManager = TypeVar('ModelManager')
class WorkerRemoveModel(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, mname, ename, mmanager:ModelManager):
        super().__init__(inst_t, dest_t, mname, ename)
        
        # X
        self.insert_input_port(WorkerRemoveConfig.model_start_port)

        # State
        self.init_state(WorkerRemoveConfig.IDLE)
        self.insert_state(WorkerRemoveConfig.IDLE, Infinite)
        self.insert_state(WorkerRemoveConfig.HANDLE, 0)

        # Domain Part
        self.model_manager = mmanager
        self.model_list = []

    def ext_trans(self, port, msg):
        if port == WorkerRemoveConfig.model_start_port:
            self.model_list.append(msg.retrieve()[0])
            self._cur_state = WorkerRemoveConfig.HANDLE
        pass
    
    def output(self):
        #print("Worker Remove")
        for model in self.model_list:
            # save human_info into the mongodb
            #print(model)
            print(f"Delete {model}")
            self.model_manager.remove_worker(model)
        
        self.model_list = []
        # Check
        return None

    def int_trans(self):
        if self._cur_state == WorkerRemoveConfig.HANDLE:
            self._cur_state = WorkerRemoveConfig.IDLE
        pass