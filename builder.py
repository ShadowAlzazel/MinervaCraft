import asyncio
import os 
import json

from javascript import require, On, Once, AsyncTask

from settings import SETTINGS

mineflayer = require('mineflayer')
minecraft_data = require('minecraft-data')
prismarine_items = require('prismarine-item')
pathfinder = require('mineflayer-pathfinder')
pvp = require('mineflayer-pvp')
collect_block = require('mineflayer-collectblock')
auto_eat = require('mineflayer-auto-eat')
armor_manager = require('mineflayer-armor-manager')
tool_plugin = require('mineflayer-tool')


MC_VERSION = SETTINGS["minecraft"]["version"]
mcdata = minecraft_data(MC_VERSION)