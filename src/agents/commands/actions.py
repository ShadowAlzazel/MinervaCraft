import asyncio
import os 
import json
from typing import Dict

from src.agents.library import world, skills

# Create actions in py form

# And have each model re format them to their type


class Action:
    def __init__(self, name: str, func: any, interruptible: bool=True, resumable: bool=False):
        self.name: str = name
        self.func: any = func
        self.interruptible: bool = interruptible
        self.resumable: bool = resumable
        
    async def run(self, bot, **kwargs):
        result = await self.func(bot, **kwargs)
        return result
    
# Actions
ACTION_MAP: Dict[str, Action] = {
    "go_to_player": Action(name="go_to_player", func=skills.go_to_player),
    "follow_player": Action(name="follow_player", func=skills.follow_player),
    "equip_item": Action(name="equip_item", func=skills.equip_item),
    "collect_blocks": Action(name="collect_blocks", func=skills.collect_blocks),
    "attack_player": Action(name="attack_player", func=skills.attack_player)
}