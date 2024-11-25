import asyncio
from javascript import require, On

# Modules
from ..models import model_manager

mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')

class Agent:

    # Initialize API and model
    def __init__(self, **profile):
        self.name = profile["name"]
        self.api = profile["api"]
        # Get then init new model
        new_model = model_manager.find_model(api=profile["api"], model=profile["model"])
        model_args = model_manager.get_model_args(**profile)
        self.model = new_model(**model_args)
        # Conversing

    # Start Bot in Minecraft
    def start(self, **kwargs):
        bot = mineflayer.createBot({
            "host": kwargs["host"],
            "port": kwargs["port"],
            "auth": kwargs["port"],
            "version": kwargs["version"],
            "username": self.name
        })
        
        
    # Chat
    async def send_chat(self, user: str, message: str):
        new_message = {
            "role": "user",
            "content": f'{user}: {message}'
        }
        
        response = await self.model.send_request(messages=[new_message])
        print(response)