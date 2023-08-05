from base.agent_model import AgentModel

class HumanAgent(AgentModel):
    def __init__(self, human_info):
        super().__init__()
        self.agent = {"id": human_info["id"], "smock": human_info["smock"], \
            "wbgt": human_info["wbgt"], "met": human_info["met"], \
                "health": human_info["health"], "out": human_info["out"]}
