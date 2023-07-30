from base.agent_model import AgentModel

class HumanAgent(AgentModel):
    def __init__(self, id, smock, wbgt, met, health, out, simulation_number):
        super().__init__()
        self.agent = {"id": id, "smock": smock, "wbgt": wbgt, \
            "met": met, "health": health, "out": out, "simulation_number": simulation_number}
