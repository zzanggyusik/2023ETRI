from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.system_simulator import SystemSimulator
from pyevsim.system_message import SysMessage
from pyevsim.definition import *

from typing import TypeVar

from config import * 

import pymongo
import datetime
import logging

ModelManager = TypeVar('ModelManager')
class WorkerModel(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, mname, ename, hinfo):
        super().__init__(inst_t, dest_t, mname, ename)
        #Env DB

        self.db_url = f"mongodb://{config['site_human_db']['db_user']}:{config['site_human_db']['db_pw']}@{config['site_human_db']['db_addr']}"
        self.db = pymongo.MongoClient(self.db_url)[config['site_human_db']['db_name']]
        self.config = config
        self.hinfo = hinfo

        # Model Management
        self.insert_input_port(mname)
        self.insert_output_port(mname)

        # Environment Management
        self.insert_input_port('env')
        self.insert_output_port('req_env')

        # Telegram Management
        self.insert_output_port("msg")
        self.insert_output_port("health_info")

        # State
        self.init_state("REQ_ENV")
        self.insert_state("REQ_ENV", 0)
        self.insert_state("WAIT", Infinite)
        self.insert_state("MONITOR", config['worker']['indv_worker_mon_freq'])

        # Domain Part
        self.engine = SystemSimulator.get_engine(ename)
        self.env_info = None
        self.timestamp = None

    def ext_trans(self, port, msg):
        if port == 'env':
            self.env_info = msg.retrieve()[0]
            self._cur_state = "MONITOR"
        pass
    
    def output(self):
        if self._cur_state == "REQ_ENV":
            return SysMessage(self.get_name(), "req_env")
        elif self._cur_state == "MONITOR":
            # TODO: Check Health
            #print(f"{self.get_name()} checking hsinfo")
            
            # TODO: update human_info, should update each field

            hsinfo = self.db[f"{self.config['site_human_db']['db_collection_name']}"].find_one({"human_id":self.hinfo["human_id"]})

            msg_lst = []
            # Check validity
            if 'timestamp' in hsinfo and hsinfo['timestamp'] == self.timestamp:
                msg = SysMessage(self.get_name(), self.get_name())
                msg.insert(self.hinfo)
                #저장할 것 다 저장하고 worker_remove(update해야함) ->worker remove에서 해줘야함, 
                msg_lst.append(msg)
            else:
                self.timestamp = hsinfo['timestamp']
                self.cal_health_score(hsinfo,self.env_info)

                msg = SysMessage(self.get_name(), "health_info")
                
                msg.insert((self.get_name(), f"{self.hinfo['health_score']}\n"))
                msg_lst.append(msg)

                state =self.check_(self.hinfo['health_score'])
                if state ==0:
                    pass
                else:
                    send=[state]
                    send = f"ID: {self.get_name()[-2:]}\n{state} '{self.hinfo['health_score']}'"
                    msg = SysMessage(self.get_name(), 'msg')
                    msg.insert((self.config["telegram_manager"]["chatID"], send))
                    msg_lst.append(msg)


                
            '''            
            # TODO: Check Health
            msg_lst = []

            if self.hinfo["health_score"] <= self.config['cal_health']['caution']:

                 msg = SysMessage(self.get_name(), 'msg')
                 msg.insert((self.config["telegram_manager"]["chatID"], "caution"))
                 msg_lst.append(msg)

            elif self.hinfo["health_score"]<=self.config['cal_health']['warning']:
                msg = SysMessage(self.get_name(), 'msg')
                msg.insert((self.config["telegram_manager"]["chatID"], "caution"))
                msg_lst.append(msg)

            else:
                msg = SysMessage(self.get_name(), 'msg')
                msg.insert((self.config["telegram_manager"]["chatID"], "~~~"))
                msg_lst.append(msg)
            '''
            return msg_lst
            
            

            print(f"{self.get_name()} checking hinfo")
            # TODO: update human_info, should update each field

        return None


    def int_trans(self):
        if self._cur_state == "MONITOR":
            self._cur_state = "MONITOR"
        elif self._cur_state == "REQ_ENV":
            self._cur_state = "WAIT"

    def cal_health_score(self,hsinfo,env_info):
        #{'_id': ObjectId('636baa733b39a4e1ae3b0357'), 'datetime': '2022-11-09 15:50:24', 'wbgt': 11.4, 'temp': 11.4, 'humid': 81.0, 'wind': 0.2}
        #{'_id': ObjectId('635e53eead92e430f1d7d0ba'), 'human_id': '412f6032-aad4-433c-b89c-a9f1755a08ee', 'smock': '000', 'work_intensive': 2, 'timestamp': '2022-11-09 15:31:53', 'health_score': 80}
        
        work = hsinfo['work_intensive']*2
        ww=self.wbgt_weight(self.env_info['wbgt'])
        sw=self.smock_weight(hsinfo['smock'])

        ins =10#증가
        des =1#감소
        print("prev", self.hinfo['health_score'])
        if work ==0:
            if self.hinfo['health_score']==100:
                pass
            elif self.hinfo['health_score'] <= self.config['cal_health']['warning']:
                ins=ins*0.5
                self.hinfo['health_score']+=ins
            else:
                ins=ins*0.7
                self.hinfo['health_score']+=ins
        else:
            if self.hinfo['health_score'] <= self.config['cal_health']['warning']:

                des += ww
                des += work
                des += int(sw)
                self.hinfo['health_score']-=des
             
            else:
                des += ww
                des += work
                des += int(sw)
                des = des*0.7
                self.hinfo['health_score']-=des

        if self.hinfo['health_score']>=100:
            self.hinfo['health_score'] =100
        else:
            pass

        print("after", self.hinfo['health_score'])

    def smock_weight(self,smock):
        if smock =='000':
            return 1
        elif smock=='001':
            return 2
        elif smock =="111":
            return 4
        else:
            return 100

    def wbgt_weight(self,wbgt):

        if wbgt >38:
            return 5
        elif wbgt >35:
            return 4
        elif wbgt > 33:
            return 3
        elif wbgt >31:
            return 2
        else:
            return 1 

    def check_(self,hs):
        if hs <= self.config['cal_health']['warning']:
            state = "WARNING"
            return state
            #elif hs<=self.config['cal_health']['caution']:
            #    state = "CAUTION"
            #return state
        else:
            return 0
        

    # insert_modle - env - checking hinfo