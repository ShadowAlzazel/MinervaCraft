import asyncio
import os 
import json
from typing import Dict

from .library import world, skills
from .commands import actions

class ActionManager:
    
    
    def __init__(self, agent):
        self.agent = agent
        # Map all actions to their respective function
        self.action_map: Dict[str, actions.Action] = actions.ACTION_MAP
        # Create the action files in memory
        self.action_list: list = []
        self._poplulate_action_params()
        # Runtime
        self.current_action = None
        self.last_action = None
        # TODO
        # Have actions be an Obj(class) that point to their respective function
        # Create a new action when requested
        # Some actions have the `interptable field`
        # Some actions require promises, or can be schedukes to run later
        # All actions have their `run` function
        
        
        
    def _poplulate_action_params(self):
        # Find all actions
        root = "src/agents/commands/actions"
        for key in self.action_map.keys():
            file_path = f'{root}/{key}.json'
            if not os.path.exists(file_path):
                continue
            obj = {}
            with open(file_path, "r") as f:
                obj = json.loads(f.read())
            # Add to list
            self.action_list.append(obj)
                
    
    def _create_new_action(self):
        # TODO 
        # Create a new function and stores it in memory and in own folder
        # The file is a runnable python command
        pass
              
                       
    def convert_args(self, arguments):
        if isinstance(arguments, dict):
            return arguments    
        else:
            json_args = json.loads(arguments)                
            return json_args
                 
            
    async def call_action(self, action_name: str, **action_kwargs):
        action = self.action_map[action_name]
        if action and action.func:
            self.last_action = self.current_action
            self.current_action = action
            result = await action.run(self.agent.bot, **action_kwargs)
        return result
        
    
    def call_wrapped_action(self, action_name: str, **action_kwargs):
        asyncio.run(call_action(action_name, **action_kwargs))