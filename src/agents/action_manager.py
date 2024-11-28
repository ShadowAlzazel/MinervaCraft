import asyncio
import os 
import json

from .library import world, skills

class ActionManager:
    
    
    def __init__(self, agent):
        self.agent = agent
        # Map all actions to their respective function
        self.action_func_map = {
            "go_to_player": skills.go_to_player,
            "follow_player": skills.follow_player
        }
        # Create the action files in memory
        self.action_list: list = []
        self._create_actions()
        # Runtime
        self.current_action = None
        # TODO
        # Have actions be an Obj(class) that point to their respective function
        # Create a new action when requested
        # Some actions have the `interptable field`
        # Some actions require promises, or can be schedukes to run later
        # All actions have their `run` function
        
        
        
    def _create_actions(self):
        # Find all actions
        root = "src/agents/commands/actions"
        for key in self.action_func_map.keys():
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
            
    async def call_action(self, func_name: str, **func_kwargs):
        func = self.action_func_map[func_name]
        await func(self.agent.bot, **func_kwargs)
        pass
        