import dill
import time
from concurrent.futures import ThreadPoolExecutor


class ExecutionEngine:
    def __init__(self, multi_count):
        self.state = "IDLE"
        self.environment = ""  # environment : source
        self.agent = ""  # agent name : source
        self.parts = []  # parts model
        self.bootloader = {}  # state : path
        self.multi_count = multi_count  # 동시 실행 parts 수

    def set_agent_source(self, source):
        self.agent = source

    def set_env_source(self, source):
        self.environment = source

    def append_bootloader(self, name, path):
        self.bootloader[name] = path

    # parts list clear
    def clear_parts(self):
        self.parts = []

    def run_parts(self, parts):
        parts.run_parts()
        # print("test")
        
    def test_run_parts(self) :
        for parts in self.parts :
            parts.run_parts()

    # parts run
    def run_multi_parts(self):
        state = self.state

        with ThreadPoolExecutor(max_workers=self.multi_count) as executor:
            executor.map(self.run_parts, self.parts)

        if state == self.state:
            # 상태가 변화할 경우 parts를 초기화한 후 새로운 boot loader를 실행함
            self.state = state
            self.clear_parts()
            self.run_boot_loader()

    def set_parts_object_data(self):
        ##model이 어떤 object가 필요한지 요청을 어떻게 할것인지?
        # 추상화와 request가 필요...
        # 어떻게..?
        for parts in self.parts:
            parts.set_agent(self.agent)
            parts.set_environment(self.environment)
        pass

    def run_boot_loader(self):
        with open(self.bootloader[self.state], "rb") as f:
            bootloader = dill.load(f)
        # 후에는 따로 불러올 방법을 고려해야함
        self.parts = bootloader.set_parts()
        self.set_parts_object_data()
