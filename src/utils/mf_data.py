import asyncio
import os 
import json

from javascript import require, On, Once, AsyncTask

from settings import SETTINGS

minecraft_data = require('minecraft-data')
mineflayer = require('mineflayer', "latest")
prismarine_items = require('prismarine-item')
pathfinder = require('mineflayer-pathfinder')
pvp = require('mineflayer-pvp')
collect_block = require('mineflayer-collectblock')
auto_eat = require('mineflayer-auto-eat')
armor_manager = require('mineflayer-armor-manager')
tool_plugin = require('mineflayer-tool')


MC_VERSION = SETTINGS["start_args"]["version"]
mcdata = minecraft_data(MC_VERSION)

# This is for mineflayer-data 

# Classes
Vec3 = require("vec3").Vec3
Item = prismarine_items(MC_VERSION)

# Methods
def get_item_id(item_name):
    """Get the item ID from the item name."""
    if item_name in mcdata.itemsByName:
        return mcdata.itemsByName[item_name].id
    return None

def get_item_name(item_id):
    """Get the item name from the item ID."""
    if item_id in mcdata.items:
        return mcdata.items[item_id].name
    return None


def get_block_name(block_id):
    """Get the block name from the block ID."""
    if block_id in mcdata.blocks:
        return mcdata.blocks[block_id].name
    return None


def get_block_id(block_name):
    """Get the block ID from the block name."""
    if block_name in mcdata.blocksByName:
        return mcdata.blocksByName[block_name].id
    return None


def get_all_items(ignore=None):
    """Get a list of all items with optional ignore parameter."""
    if ignore is None:
        ignore = []
    items = []
    for item_id, item in mcdata.items.items():
        if item.name not in ignore:
            items.append(item)
    return items


def get_all_item_ids(ignore=None):
    """Get a list of all item IDs with optional ignore parameter."""
    items = MinecraftData.get_all_items(ignore)
    item_ids = [item.id for item in items]
    return item_ids


def get_all_blocks(ignore=None):
    """Get a list of all blocks with optional ignore parameter."""
    if ignore is None:
        ignore = []
    blocks = []
    for block_id, block in mcdata.blocks.items():
        if block.name not in ignore:
            blocks.append(block)
    return blocks


def get_all_block_ids(ignore=None):
    """Get a list of all block IDs with optional ignore parameter."""
    blocks = MinecraftData.get_all_blocks(ignore)
    block_ids = [block.id for block in blocks]
    return block_ids