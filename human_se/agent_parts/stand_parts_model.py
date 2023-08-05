from base.parts_model import PartsModel
import dill
import time
import pymongo

class StandPartsModel(PartsModel):
    def __init__(self, simulation_number):
        super().__init__()
        self._simulation_number = simulation_number
        self.count = 0
        
    def run_parts(self):
        # time.sleep(0.5)
        self.agent["health"] -= 4
        print("Stand..")
        print("current state", self.agent)
        # print("env test", self.environment)
        print("")
        
        if self.count == self._simulation_number:
            print("simulation finished")
            
    def build_parts_model(self):
        loader = StandPartsModel(self._simulation_number)
        with open("./parts/sit_parts_model.simx", "wb") as f:
            dill.dump(loader, f)

# 수동 생성
if __name__ == "__main__":
    loader = StandPartsModel()
    with open("./parts/stand_parts_model.simx", "wb") as f:
        dill.dump(loader, f)