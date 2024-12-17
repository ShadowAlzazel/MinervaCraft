import asyncio
import multiprocessing
from javascript import On, Once, AsyncTask, start, stop, abort

from .agents.agent import Agent


# Holder Class for agents 
# Async calls made from TaskGroup called here
class AgentProcess:
    
    def __init__(self, agent: Agent, **settings):
        self.agent = agent
        self.settings = settings
        # Events
        self.agent.process = self
    
    # Start the bot and conenct using mineflayer
    async def run_bot(self) -> None:
        # Setting up bot
        self.agent.init_bot(**self.settings)
        print(f'{self.agent.name} started bot {self.agent.name} using mineflayer!')
        # Run the main loop
        await self.agent.run()
        
    # Main Entry point for runner 
    async def run(self) -> None:
        # Logging In
        try:
            await self.run_bot()
        except Exception as error:
            self.agent.stop_agent()
            print(f'Agent Error: {error} - Restarting')
            asyncio.sleep(2) # Wait a little
            await self.run_bot()
            
