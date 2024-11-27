import asyncio

from javascript import require, On, Once
from ...utils.wrappers import RunAsync
from .world import *

mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')

async def go_to_player(
    bot,
    player_name: str,
    max_distance: float=32.0,
    closeness: float=3):
    # Get player
    player = bot.players[player_name]
    if not player:
        return False
    if not player.entity:
        return False
    # Check if near
    bot_pos = bot.entity.position
    pos = player.entity.position
    distance = player.entity.position.distanceTo(bot_pos)
    if distance > max_distance:
        return False
    # Start movement
    move = pathfinder.Movements(bot)
    bot.pathfinder.setMovements(move)
    bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, 0.5))
    
    
async def follow_player(
    bot,
    player_name: str,
    max_distance: float=32.0,
    closeness: float=3):
    # Get player
    player = bot.players[player_name]
    if not player:
        return False
    if not player.entity:
        return False
    bot_pos = bot.entity.position
    pos = player.entity.position
    distance = player.entity.position.distanceTo(bot_pos)
    if distance > max_distance:
        return False
    # Start follow
    move = pathfinder.Movements(bot)
    bot.pathfinder.setMovements(move)
    goal = pathfinder.goals.GoalFollow(player.entity, closeness)
    bot.pathfinder.setGoal(goal, True)    
    
    
async def attack_nearest_entity(
    bot,
    entity_name: str, 
    kill: bool,
    max_distance: float=5.0):
    # Find
    nearest = get_nearby_entities(bot, [], [entity_name], max_distance)
    if not nearest: 
        return
    