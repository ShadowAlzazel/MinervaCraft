import asyncio

from javascript import require, On, Once
from ...utils.wrappers import RunAsync

# entity_types = ["animal, player, hostile"]

def get_nearby_entities(
    bot, 
    entity_types: list=["animal"],
    entity_names: list=["chicken"],
    max_distance: float=16): 
    # Set a distance
    if not max_distance:
        max_distance = 16
    nearby = []
    position = bot.entity.position
    # null check
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
     
    nearby.sort(key=lambda entry: entry["distance"])
    return nearby


def get_nearest_blocks(
    bot,
    block_types: list[str],
    distance,
    count):
    pass


