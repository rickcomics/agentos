from .agent import Agent
def load_agent(agent_name):
    """
    Загружает класс агента по имени из его папки.
    Ожидается, что в папке есть agent.py с классом Agent.
    """
    module_name = f"agents.{agent_name}.agent"
    module = __import__(module_name, fromlist=["Agent"])
    return module.Agent