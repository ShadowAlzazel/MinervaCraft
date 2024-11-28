import asyncio
import os 
import json

from javascript import require, On, Once, AsyncTask

# Abs
from src.utils import mf_data as mf
from src.utils.wrappers import RunAsync
# Rel
from . import memory_controller, action_manager, prompters
from .library import skills, world
from .commands import actions


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
            new_model = prompters.find_model(api=profile["api"], model=profile["model"])
            model_args = prompters.get_model_args(**profile)
            model_args["commands"] = self.action_manager.action_list
            self.model = new_model(**model_args)
            print(f'[{self.name}] Loaded new client ({self.api}) with the model ({self.model.model})')
            # Create memory controller
            self.memory = memory_controller.MemoryController(self) 
            # Create new model api from profile
            # Success
            print(f'Initialized agent: [{self.name}]')
        # Error
        except Exception as error:
            print(f'Failed to initialize agent: {error}')
            

    # Start Bot in Minecraft
    def start_bot(self, **kwargs):
        bot = mf.mineflayer.createBot({
            "host": kwargs["host"],
            "port": kwargs["port"],
            "auth": kwargs["port"],
            "version": kwargs["version"],
            "username": self.name
        })
        self.bot = bot
        # Plugins
        self.bot.loadPlugin(mf.pathfinder.pathfinder)
        self.bot.loadPlugin(mf.pvp.plugin)
        self.bot.loadPlugin(mf.collect_block.plugin)
        self.bot.loadPlugin(mf.tool_plugin.plugin)
        #self.bot.loadPlugin(mf.auto_eat.plugin)
        #self.bot.loadPlugin(mf.armor_manager.plugin)
        # Logging In
        print(f'{self.name} has logged on to Minecraft!')


    # Method to access new information
    # TODO
    # request from INTERNET


    # Prompt
    @RunAsync
    async def prompt_chat(self, user: str, message: str):
        response = await self.model.send_prompt(f'{user}: {message}')
        content = response.content
        if content:
            self.bot.chat(content)
        # TEMP
        # TODO
        # CREATE MAIN CHECKER FOR TOOL COOLS LATER
        if response.tool_calls:
            tool_call = response.tool_calls[0]
            func_name = tool_call.function.name
            arguments = tool_call.function.arguments
            print(f'{self.name} called function {func_name}')
            print(f'Args: {arguments}')
            fkwargs = self.action_manager.convert_args(arguments)
            await self.action_manager.call_action(func_name, **fkwargs)

        
    # Run this method LAST
    async def run(self):
        bot = self.bot
        # Loading instructions
        await self.model.send_request(self.model.instructions, "system")
     
        # Basic Chat Handler
        @On(bot, "chat")
        def handle(this, username: str, message: str, *args):
            # Ignore self
            if username == bot.username:
                return
            # Ignore commands
            if message[0] == "/":
                return
            
            player = bot.players[username]
            print(f'{username} said: {message}')
            match message:
                case "Hello":
                    bot.chat("Hello World!")
                case "come" | "Come":
                    skills.go_to_player(bot, username, 20.0)
                case "follow" | "Follow":
                    skills.follow_player(bot, username, 20.0)
                case "blocks":
                    world.get_nearest_blocks(bot, ["grass_block"])
                case "mine":
                    skills.collect_blocks(bot, "grass_block")
                case "equip":
                    skills.equip_item(bot, "diamond_shovel")
                case "fight":
                    bot.pvp.attack(player.entity)
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

        