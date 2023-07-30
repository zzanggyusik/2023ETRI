from rx import create

class AgentModel:
    def __init__(self):
        self.agent = {}

    def get_source(self):
        print(self.agent)
        return create(self.object_rx)

    def object_rx(self, observer, scheduler):
        observer.on_next(self.agent)
        observer.on_completed()
