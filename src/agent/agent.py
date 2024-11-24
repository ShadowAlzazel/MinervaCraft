import asyncio

from javascript import require, On
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')

class Agent:

    def __init__(self, name: str="gpt"):
        self.name = name


    def start(self, **kwargs):
        bot = mineflayer.createBot({
            "host": kwargs["host"],
            "port": kwargs["port"],
            "auth": kwargs["port"],
            "version": kwargs["version"],
            "username": self.name
        })