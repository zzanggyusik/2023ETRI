from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.system_simulator import SystemSimulator
from pyevsim.system_message import SysMessage
from pyevsim.definition import *

from config import *

from telegram import * 
from telegram.ext import *

class TelegramManagerModel(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, mname, ename, engine):
        super().__init__(inst_t, dest_t, mname, ename)

        self.engine = engine
        
        # X
        self.insert_input_port('alert')

        # State
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("HANDLE", 0)

        # Domain Part
        self.alert_msg_list = []

        # Telegram Part
        self.updater = Updater(TelegramConfig.token)

    def ext_trans(self, port, msg):
        if port == 'alert':
            print("@@")
            self.alert_msg_list.append(msg.retrieve()[0])
            self._cur_state = "HANDLE"
        pass
    
    def output(self):
        print("self.alert_msg_list")
        for msg in self.alert_msg_list:
            print(msg[0], msg[1])
            self.updater.bot.send_message(msg[0], text=(msg[1]))
            
        self.alert_msg_list = []
        # Check
        return None

    def int_trans(self):
        if self._cur_state == "HANDLE":
            self._cur_state = "IDLE"
        pass