import asyncio
import os 
import json

from javascript import On, Once, AsyncTask, start, stop, abort

# Abs
from src.utils import mf_data as mf
#from src.utils.wrappers import EventHandler
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
            self.username = profile["username"] # The username of the microsoft account 
            self.process = None
            # For Async Events
            self._running = True
            self.event_queue = asyncio.Queue()
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
            # Start model and api
            self.api = profile["api"]
            # Create new model api from profile
            new_model = prompters.find_model(api=profile["api"], model=profile["model"])
            model_args = prompters.get_model_args(**profile)
            model_args["commands"] = self.action_manager.action_list
            self.model = new_model(**model_args)
            print(f'[{self.name}] Loaded new client ({self.api}) with the model ({self.model.model})')
            # Create memory controller
            self.memory = memory_controller.MemoryController(self) 
            # Async 
            self.events = []
            # Success
            print(f'Initialized agent: [{self.name}]')
        # Error
        except Exception as error:
            print(f'Failed to initialize agent {profile["name"]}: {error}')
            

    # Start Bot in Minecraft
    def init_bot(self, **kwargs):
        bot = mf.mineflayer.createBot({
            "username": self.username,
            
            "host": kwargs["host"],
            "port": kwargs["port"],
            "auth": kwargs["auth"],
            "version": kwargs["version"]
        })
        self.bot = bot
        # Plugins
        self.bot.loadPlugin(mf.pathfinder.pathfinder)
        self.bot.loadPlugin(mf.pvp.plugin)
        self.bot.loadPlugin(mf.collect_block.plugin)
        self.bot.loadPlugin(mf.tool_plugin.plugin)
        #self.bot.loadPlugin(mf.auto_eat.plugin)
        #self.bot.loadPlugin(mf.armor_manager.plugin)
    
    # Create aMethod to access new information
    # TODO -> request from INTERNET information like wiki or tutorials
    
    # Prompt
    async def send_prompt(self, user: str, message: str):
        response = await self.model.send_prompt(f'{user}: {message}')
        content = response.content
        if content:
            self.bot.chat(content)
        # TEMP
        # TODO
        # CREATE MAIN CHECKER FOR TOOL COOLS LATER
        # FIX this CALL, currently times out
        if response.tool_calls:
            tool_call = response.tool_calls[0]
            func_name = tool_call.function.name
            arguments = tool_call.function.arguments
            print(f'{self.name} called function {func_name}')
            print(f'Args: {arguments}')
            fkwargs = self.action_manager.convert_args(arguments)
            await self.action_manager.call_action(func_name, **fkwargs)


    # Process the user and message and do stuff 
    async def process_chat(self, username: str, message: str, *args):
        match message:
            case "Hello":
                self.bot.chat("Hello World!")
            case "come" | "Come":
                #self.action_manager.call_wrapped_action(username, 20.0)
                await skills.go_to_player(self.bot, username, 20.0)
            case "follow" | "Follow":
                await skills.follow_player(self.bot, username, 20.0)
            case "blocks":
                world.get_nearest_blocks(self.bot, ["stone"])
            case "mine":
                await skills.collect_blocks(self.bot, "oak_log")
            case "equip":
                await skills.equip_item(self.bot, "diamond_pickaxe")
            case "fight":
                await skills.attack_player(self.bot, username)
            case "near":
                nearby = world.get_nearby_entities(self.bot, entity_types=["animal"])
                print(nearby)
            case _:
                await self.send_prompt(username, message)
  
  
    # Handle Messages (ignore self, commands)
    async def chat_handler(self, username: str, message: str, *args):
        # Ignore messages from self
        if username == self.bot.username:
            return
        # Ignore commands
        if message.startswith("/"):
            return
        # Ensure the player exists
        print(f'{username} said: {message}')
        if username in self.bot.players:
            player = self.bot.players[username]
            await self.process_chat(username, message, *args)
        else:
            print(f"Player {username} not found in bot players.")


    async def handle_events(self):
        while self._running:
            print(f'Queue: {self.event_queue.qsize()}')
            queue_empty = self.event_queue.qsize() <= 0
            if not queue_empty:
                print("Fetching Event...")
                event = await self.event_queue.get()  # Wait for an event from the queue
                # Get the next event from the queue
                username, message, args = event
                print("Handling Event")
                await self.chat_handler(username, message, *args)
                self.event_queue.task_done()
            else:
                await asyncio.sleep(0.5)

    # Run the bot
    async def run(self):
        bot = self.bot
        print(f'Agent Event Loop Started')
        # Start the event handler loop
        #loop = asyncio.get_running_loop()
        #loop.run_forever()
        event_handler = asyncio.create_task(self.handle_events())

        # On Chat
        @On(bot, "chat")
        def chat(this, username: str, message: str, *args):
            nonlocal self  # Ensure self is accessible
            # Create a task for the async function
            self.event_queue.put_nowait((username, message, args))
        

        # On Spawn
        @Once(bot, "spawn")
        def spawn(this):
            nonlocal self
            print(f'The Agent {self.name} has Spawned!')
            bot.chat("Hi! I have arrived.")