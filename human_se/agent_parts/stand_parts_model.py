from base.parts_model import PartsModel
import dill
import time

class StandPartsModel(PartsModel):
    def __init__(self):
        super().__init__()
        self.count = 0
        
    def run_parts(self):
        # time.sleep(0.5)
        self.agent["hp"] -= 4
        print("Stand..")
        print("current state", self.agent)
        print("current count", self.agent["simulation_number"])
        # print("env test", self.environment)
        
        
        # if self.agent["simulation_number"] == self._simulation_number:
        #     # coll_name = f"{self.agent['container_id']}_{self.agent['seed']}"
        #     # self.collection = self._human_db[coll_name]
        #     # print("Sit simulation finished")
            
    def build_parts_model(self):
        loader = StandPartsModel()
        with open("./parts/sit_parts_model.simx", "wb") as f:
            dill.dump(loader, f)

# 수동 생성
if __name__ == "__main__":
    loader = StandPartsModel()
    with open("./parts/stand_parts_model.simx", "wb") as f:
        dill.dump(loader, f)