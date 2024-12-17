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
        self._event_queue: asyncio.Queue = asyncio.Queue()
    

    # Background task to process events
    async def event_processor(self):
        print("Started Event Processor Queue")
        while True:
            print("Waiting for work")
            func, args, kwargs = await self._event_queue.get()
            print(f"Got work: {func}, starting work")
            await func(*args, **kwargs)
            print("Work Done")
            self._event_queue.task_done() 
             
    
    # Add event to queue        
    def add_event(self, func, *args, **kwargs):
        print(self._event_queue.qsize)
        #loop = asyncio.get_running_loop()
        #asyncio.run_coroutine_threadsafe(self._event_queue.put((event_name, args, kwargs)), loop)
        self._event_queue.put_nowait((func, args, kwargs))
        print(f"Adding func {func} to event queue")
        #self._event_queue.put((func, args, kwargs))
        
    
    async def start_process(self) -> None:
        # Logging In
        self.agent.init_bot(**self.settings)
        print(f'{self.agent.name} started bot {self.agent.name} using mineflayer!')
        # Run
        await self.agent.run()
        
