import asyncio
import multiprocessing

from .agents.agent import Agent


# Holder Class for agents 
# Async calls made from TaskGroup called here
class AgentProcess:
    
    def __init__(self, agent: Agent, **settings):
        self.agent = agent
        self.settings = settings
    
    async def agent_task(self):
        # Logging In
        self.agent.start_bot(**self.settings)
        print(f'{self.agent.name} has logged on to Minecraft!')
        # Run
        await self.agent.run()