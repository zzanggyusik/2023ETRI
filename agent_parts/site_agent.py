from base.agent_model import AgentModel

class SiteAgent(AgentModel):
    def __init__(self, site_info):
        super().__init__()
        self.agent = {"site_id" : site_info["site_id"]}
