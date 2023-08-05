from base.parts_model import PartsModel
import dill
import time

class SitPartsModel(PartsModel):
    def __init__(self):
        super().__init__()
        self.count = 0
        
    def run_parts(self):
        # time.sleep(0.5)
        # Count Simulation Process
        # self.agent["simulation_number"] += 1
        
        # Calculate Health
        self.agent["health"] += 1
        print("Sit..")
        print("current state", self.agent)
        print("current count", self.agent["simulation_number"])
        
        # if self.agent["simulation_number"] == self._simulation_number:
        #     print("Sit simulation finished")

    def build_parts_model(self):
        loader = SitPartsModel()
        with open("./parts/sit_parts_model.simx", "wb") as f:
            dill.dump(loader, f)

# 수동 생성
if __name__ == "__main__":
    loader = SitPartsModel()
    with open("./parts/sit_parts_model.simx", "wb") as f:
        dill.dump(loader, f)