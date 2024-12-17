import asyncio
import multiprocessing

from .agents.agent import Agent


# Holder Class for agents 
# Async calls made from TaskGroup called here
class AgentProcess:
    
    def __init__(self, agent: Agent, **settings):
        self.agent = agent
        self.settings = settings
    
    async def start(self):
        # Logging In
        self.agent.init_bot(**self.settings)
        print(f'{self.agent.name} started bot {self.agent.name} using mineflayer!')
        # Run
        self.agent.run()