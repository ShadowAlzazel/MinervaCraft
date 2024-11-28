import asyncio

from .agents.agent import Agent


# Holder Class for agents 
# Async calls made from TaskGroup called here
class AgentProcess:
    
    def __init__(self, agent: Agent):
        self.agent = agent
    
    
    def start_bot(self, **settings):
        self.agent.start_bot(**settings)
    
    
    async def agent_task(self):
        await self.agent.run()