from base.parts_model import PartsModel
import dill
import time

class StateCheck(PartsModel):
    def __init__(self):
        super().__init__()

    def run_parts(self):
        time.sleep(0.5)
        print("state", self.agent)

if __name__ == "__main__":
    loader = StateCheck()
    with open("./parts/state_check.simx", "wb") as f:
        dill.dump(loader, f)
