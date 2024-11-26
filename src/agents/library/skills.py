import asyncio

from javascript import require, On, Once
from ...utils.wrappers import RunAsync

mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')

@RunAsync
async def go_to_player(
    bot,
    username: str,
    max_distance: float=10.0,
    closeness: float=3):
    # Get player
    player = bot.players[username]
    if not player:
        return False
    if not player.entity:
        return False
    bot_pos = bot.entity.position
    pos = player.entity.position
    distance = player.entity.position.distanceTo(bot_pos)
    if distance > max_distance:
        return False
    
    move = pathfinder.Movements(bot)
    bot.pathfinder.setMovements(move)
    bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, 0.5))