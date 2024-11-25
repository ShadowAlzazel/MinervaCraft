import asyncio
from javascript import require, On, Once, AsyncTask

# Modules
from ..models import model_manager
from ..utils.wrappers import RunAsync

mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')

class Agent():

    # Initialize API and model
    def __init__(self, **profile):
        self.name = profile["name"]
        self.api = profile["api"]
        # Get then init new model
        new_model = model_manager.find_model(api=profile["api"], model=profile["model"])
        model_args = model_manager.get_model_args(**profile)
        self.model = new_model(**model_args)
        # Success
        print(f'Initialized Agent: [{self.name}] using: [{profile["model"]}]')


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
        
        
    # Get Raw Response
    @RunAsync
    async def request_response(self, user: str, message: str, role: str="user"):
        new_message = {
            "role": role,
            "content": f'{user}: {message}'
        }
        response = await self.model.get_completion(messages=[new_message])
        print(response)
        
        
    # Chat 
    @RunAsync
    async def send_chat(self, user: str, message: str, role: str="user"):
        new_message = {
            "role": role,
            "content": f'{user}: {message}'
        }
        chat_message = await self.model.get_message(messages=[new_message])
        self.bot.chat(chat_message.content)
        
        
    # Run this method LAST
    async def run(self):
        bot = self.bot
        # Plugins
        bot.loadPlugin(pathfinder.pathfinder)
        movements = pathfinder.Movements(bot)

        
        # Basic Chat Handler
        @On(bot, "chat")
        def handle(this, username: str, message: str, *args):
            # Ignore self
            if username == bot.username:
                return
            # Ignore commands
            if message[0] == "/":
                return
            
            #print(f'{username} said: {message}')
            match message:
                case "Hello":
                    bot.chat("Hello World!")
                case "Follow" | "follow":
                    player = bot.players[username]
                    nearby = bot.entities
                    print(player) 
                    target = player.entity
                    print(target)
                    if not target:
                        return
                    pos = target.position
                    print(pos)
                    bot.pathfinder.setMovements(movements)
                    bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, 1))
                    
                case _:
                    self.send_chat(username, message)
                    pass
        
        # On Spawn
        @On(bot, "spawn")
        def spawn(this):
            nonlocal self
            self.request_response("system", "You have logged into the server!", "system")
            print(f'The Agent {self.name} has Spawned!')
            bot.chat("Hi! I have arrived.")

        