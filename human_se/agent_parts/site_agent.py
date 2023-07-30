from base.agent_model import AgentModel

class SiteAgent(AgentModel):
    def __init__(self, name, site):
        super().__init__()
        self.agent = {"name": name, "site" : site}
