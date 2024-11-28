import asyncio

from javascript import require, On, Once
from src.utils.wrappers import RunAsync
from src.utils import mcdata as mc
from . import world


async def go_to_player(
    bot,
    player_name: str,
    max_distance: float=32.0,
    closeness: float=3):
    """
        Goes to a players location using mineflayer pathfinder.

        Args:
            bot (object): The bot instance that will be executing this function. This object should have access to its own players, as well as an entity with a position.
            player_name (str): The name of the player to follow.
            max_distance (float, optional): The maximum distance in blocks at which the bot will follow the player. Defaults to 32.0.
            closeness (float, optional): The minimum closeness required between the bot and the player to continue following them. Defaults to 3.

        Returns:
            bool: Whether the bot was able to successfully follow the player.
    """
    # Get player
    player = bot.players[player_name.lower()]
    if not player:
        return False
    if not player.entity:
        return False
    # Check if near
    bot_pos = bot.entity.position
    pos = player.entity.position
    distance = player.entity.position.distanceTo(bot_pos)
    if distance > float(max_distance):
        return False
    # Start movement
    move = mc.pathfinder.Movements(bot)
    bot.pathfinder.setMovements(move)
    bot.pathfinder.setGoal(mc.pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, flaot(closeness)))
    
    
async def follow_player(
    bot,
    player_name: str,
    max_distance: float=32.0,
    closeness: float=3):
    """
        Follows a player in-game.
        Uses mineflayer pathfinder to track the movement of a player in-game.

        Args:
            bot (object): The bot instance that will be executing this function. This object should have access to its own players, as well as an entity with a position.
            player_name (str): The name of the player to follow.
            max_distance (float, optional): The maximum distance in blocks at which the bot will follow the player. Defaults to 32.0.
            closeness (float, optional): The minimum closeness required between the bot and the player to continue following them. Defaults to 3.

        Returns:
            bool: Whether the bot was able to successfully follow the player.
    """
    # Get player
    player = bot.players[player_name]
    if not player:
        return False
    if not player.entity:
        return False
    # Get the distnace between the bot and the player and checks if player is too far away
    bot_pos = bot.entity.position
    pos = player.entity.position
    distance = player.entity.position.distanceTo(bot_pos)
    if distance > float(max_distance):
        return False
    # Start follow
    move = mc.pathfinder.Movements(bot)
    bot.pathfinder.setMovements(move)
    goal = mc.pathfinder.goals.GoalFollow(player.entity, float(closeness))
    bot.pathfinder.setGoal(goal, True)    
    

async def equip_tool(
    bot,
    
    material: str,
):
    pass


@RunAsync
async def collect_blocks(
    bot,
    block_types: str,
    amount: int=5,
    ignore: list[str]=None
):
    if amount < 1:
        return False 
    
    # TODO: Get from a tag list or mc-meta-data in the future
    # Block types can be a #tag or name
    block_names = [block_types]
    # Ensure block_names is a list
    if not isinstance(block_names, list):
        block_names = [block_names]
    
    # Create a main list of nearest blocks
    nearest_blocks = world.get_nearest_blocks(bot, block_names, 16)
    # Filter if ignore
    if ignore:
        nearest_blocks = [x for x in nearest_blocks if x not in ignore]
    # Max can collect constrained by amount and avilable
    collected = 0
    avilable = min(amount, len(nearest_blocks))
    while collected < avilable:
        # Movement
        movements = mc.pathfinder.Movements(bot)
        movements.dontMineUnderFallingBlock = False
        safe_to_break = [x for x in nearest_blocks if movements.safeToBreak(x)]
        # Create a sublist to compare
        
        # Check if list emptty
        if not safe_to_break:
            break
        # Tool
        block = safe_to_break[0]
        nearest_blocks.remove(block)
        print(f'Block {block}')
        #print(bot.tool)
        bot.tool.equipForBlock(block)
        item_id = bot.heldItem 
        print(f'Item {bot.heldItem}')
        #bot.equip(item, 'hand')
        # Using block data find `material`
        # Then check inventory for the material
        # then equip
        
        #if item_id:
        #    item_id = bot.heldItem.type
        # Check if can harvest
        #if not block.canHarvest(item_id):
        #    # TODO
        #    # DO A CHECK FOR ALL TYPES
        #    continue    
        try:
            bot.collectBlock.collect(block)
            collected += 1
        except Exception as error:
            print(f'Error while collecting block: {error}')
            return False
        
        # Bot interrupt action
        # Cerate action current 
    
@RunAsync
async def attack_nearest_entity(
    bot,
    entity_name: str, 
    kill: bool,
    max_distance: float=5.0):
    # Find
    nearest = get_nearby_entities(bot, [], [entity_name], max_distance)
    if not nearest: 
        return
    