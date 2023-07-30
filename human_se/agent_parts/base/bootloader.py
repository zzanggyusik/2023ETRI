import dill
from abc import abstractmethod

class BootLoader:
    def __init__(self):
        self.state = "IDLE"
        self.parts = []
        pass

    def set_parts(self):
        data = []
        for key in self.parts:
            with open(f"./parts/{key}", "rb") as f:
                data.append(dill.load(f))
        return data
