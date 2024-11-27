import asyncio
import os 
import json

from javascript import require, On, Once, AsyncTask

# Relative
from ..models import model_manager
from . import memory_controller
from . import action_manager
from .library import skills, world
from .commands import actions
from ..utils.wrappers import RunAsync

mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')

class Agent():

    # Initialize API and model
    def __init__(self, **profile):
        try:
            # Start
            self.name = profile["name"]
            # Create bot dir 
            root = f'bots/{self.name}'
            if not os.path.exists(root):
                os.makedirs(root)
            # Profiles
            last_profile = {}
            profile_path = f'{root}/last_profile.json'
            if os.path.exists(profile_path):
                with open(profile_path, "r") as f:
                    last_profile = json.loads(f.read())   
            # Actions
            self.action_manager = action_manager.ActionManager(self) 
            # Start model
            self.api = profile["api"]
            new_model = model_manager.find_model(api=profile["api"], model=profile["model"])
            model_args = model_manager.get_model_args(**profile)
            model_args["commands"] = self.action_manager.action_list
            self.model = new_model(**model_args)
            # Create memory controller
            self.memory = memory_controller.MemoryController(self) 
            # Create new model api from profile
            # Success
            print(f'Initialized Agent Model: [{self.name}] using: [{profile["model"]}]')
        # Error
        except Exception as error:
            print(f'Failed to initialize agent: {error}')
            

    # Start Bot in Minecraft
    def start(self, **kwargs):
        bot = mineflayer.createBot({
            "host": kwargs["host"],
            "port": kwargs["port"],
            "auth": kwargs["port"],
            "version": kwargs["version"],
            "username": self.name
        })
        self.bot = bot
        print(f'{self.name} has logged on to Minecraft!')


    # Prompt
    @RunAsync
    async def prompt_chat(self, user: str, message: str):
        response = await self.model.send_prompt(f'{user}: {message}')
        content = response.content
        if content:
            self.bot.chat(content)
        # TEMP
        # CREATE MAIN CHECKER FOR TOOL COOLS LATER
        if response.tool_calls:
            tool_call = response.tool_calls[0]
            #tool_obj = json.loads(tool_call.function)
            func_name = tool_call.function.name
            fkwargs = json.loads(tool_call.function.arguments)
            await self.action_manager.call_action(func_name, **fkwargs)
        # TODO
        # request from INTERNET
        
        
    # Run this method LAST
    async def run(self):
        bot = self.bot
        # Loading instructions
        await self.model.send_request(self.model.instructions, "system")
        
        # Plugins
        bot.loadPlugin(pathfinder.pathfinder)
        
        # Basic Chat Handler
        @On(bot, "chat")
        def handle(this, username: str, message: str, *args):
            # Ignore self
            if username == bot.username:
                return
            # Ignore commands
            if message[0] == "/":
                return
            
            print(f'{username} said: {message}')
            match message:
                case "Hello":
                    bot.chat("Hello World!")
                case "come" | "Come":
                    skills.go_to_player(bot, username, 20.0)
                case "follow" | "Follow":
                    skills.follow_player(bot, username, 20.0)
                case "near":
                    nearby = world.get_nearby_entities(bot, entity_types=["animal"])
                    print(nearby)
                case _:
                    self.prompt_chat(username, message)
                    pass
        
        # On Spawn
        @On(bot, "spawn")
        def spawn(this):
            nonlocal self
            self.request_response("system", "You have logged into the server!", "system")
            print(f'The Agent {self.name} has Spawned!')
            bot.chat("Hi! I have arrived.")

        