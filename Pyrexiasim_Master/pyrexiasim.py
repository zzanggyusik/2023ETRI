#from instance import config
from pyevsim.system_simulator import SystemSimulator
from pyevsim.definition import Infinite
from pyrexiasim_manager import ModelManager
from telegram_manager import TelegramManagerModel
from config import *

import json

class PyrexiaSim():
    def __init__(self):
        self.ss = SystemSimulator()
        ename = Init.enmae
        self.engine = self.ss.register_engine(ename, Init.simulation_time, Init.simulation_unit_time)
        self.tmanager = TelegramManagerModel(0, Infinite, Init.telegram_manager_name, ename, self.engine)
        self.mmanager = ModelManager(0, Infinite, Init.model_manager_name, ename, self.engine, self.tmanager)

    def start(self):
        self.engine.simulate()

if __name__ == "__main__":
    pysim = PyrexiaSim()
    pysim.start()