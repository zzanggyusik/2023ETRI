from base.bootloader import BootLoader
import dill

class HumanBootLoader(BootLoader):
    def __init__(self, parts_list):
        super().__init__()
        self.state = "SIMULATE"
        self.parts = parts_list

    # bootloader build 함수 호출
    def build_bootloader(self):
        loader = HumanBootLoader(self.parts)
        with open("./bootloader/human_boot_loader.simx", "wb") as f:
            dill.dump(loader, f) 
    

# 수동 생성
if __name__ == "__main__":
    loader = HumanBootLoader()
    with open("./bootloader/human_boot_loader.simx", "wb") as f:
        dill.dump(loader, f)
