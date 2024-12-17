import asyncio
import math

from src.utils import mf_data as mf

# entity_types = ["animal, player, hostile"]

def get_nearby_entities(
    bot, 
    entity_types: list=["animal"],
    entity_names: list=["chicken"],
    max_distance: float=16): 
    """
        Get a list of entities within a specified distance from the bot.

        Args:
            bot (Bot): The Minecraft bot instance that will perform the entity search.
            entity_types (List[str], optional): A list of entity types to search for. Defaults to ["animal"].
            entity_names (List[str], optional): A list of entity names to search for. Defaults to ["chicken"].
            max_distance (float, optional): The maximum distance within which to search for entities. Defaults to 16.

        Returns:
            List[Dict]: A list of dictionaries containing information about the nearby entities, including their type and name.

        Raises:
            ValueError: If max_distance is not a positive number.
    """
    # Set a default value for max_distance if it's not provided
    if not max_distance or max_distance <= 0:
        raise ValueError("max_distance must be a positive number")

    nearby = []
    position = bot.entity.position

    # Get the list of entities from the bot
    entities = bot.entities
    if not entities:
        return []
    for entry in bot.entities:
        entity = bot.entities[entry]
        if not entity:
            continue
        # Ignore self
        if entity.type == "player" and entity.username == bot.username:
            continue
        distance = entity.position.distanceTo(position)
        if distance > max_distance:
            continue
        # Either can be true
        if entity.type in entity_types or entity.name in entity_names:
            nearby.append({"entity": entity, "distance": distance})
    # Sort the list by distance
    nearby.sort(key=lambda entry: entry["distance"])
    return nearby


def get_nearest_blocks(
    bot,
    block_names: list[str],
    distance: int=16,
    count: int=1000,
    ignore: list[str]=None):
    """
        Get a list of the nearest blocks of the given types.

        Args:
            bot: The bot to get the nearest block for.
            block_names (List[str], optional): The names of the blocks to search for. Defaults to None.
            distance (int, optional): The maximum distance to search, default 16.
            count (int, optional): The maximum number of blocks to find, default 10000.
            ignore (List[str], optional): The blocks to ignore.

        Returns:
            List[Block]: The nearest blocks of the given type.
    """
    block_ids = []
    # If block_names is not a list, make it a list
    if block_names is None:
        block_ids = mf.getAllBlockIds(['air'])
    else:
        # Ensure block_names is a list
        if not isinstance(block_names, list):
            block_names = [block_names]
        # Get block IDs from the block types
        for name in block_names:
            block_ids.append(mf.get_block_id(name))
    # Get the positions of the matching blocks
    positions = bot.findBlocks({
        'matching': block_ids,
        'maxDistance': distance,
        'count': count
    })
    blocks = []
    # Process each position to get the nearest block
    bot_position = bot.entity.position
    for position in positions:
        block = bot.blockAt(position)
        distance_to_bot = position.distanceTo(bot_position)
        # Store the block and its distance to the bot
        blocks.append({'block': block, 'distance': distance_to_bot})
    
    # Sort the blocks by their distance to the bot
    blocks.sort(key=lambda entry: entry['distance'])
    # Return only the first sqrt(amount) blocks (without their distances)
    amount_root = int(math.sqrt(count))
    return [b['block'] for b in blocks[:10]]


