import os 
import json

class MemoryController:
    
    def __init__(self, agent):
        # Link
        self.agent = agent
        # Create sub dir for memories
        bot_path = f'bots/{self.agent.name}'
        if not os.path.exists(f'{bot_path}/memories'):
            os.makedirs(f'{bot_path}/memories')
        if not os.path.exists(f'{bot_path}/histories'):
            os.makedirs(f'{bot_path}/histories')
        
        self.memories: list[dict] = []
