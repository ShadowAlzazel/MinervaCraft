import sys
import os 
import json
import asyncio

from javascript import require, On

# Main 
from settings import SETTINGS
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')

# Modules
from src.agent.agent import Agent


def get_profiles() -> list[dict]:
    default = "profiles/default.json"
    profiles = []
    for profile in SETTINGS["profiles"]:
        # Find filepath
        file_path = f'profiles/{profile}.json'
        if os.path.exists(file_path):
            print(f'Found profile for [{profile}], loading it.')
        else:
            print(f'Did not find profile for [{profile}], skipping...')
            continue
        # Open profile json
        with open(file_path, "r") as f:
            obj = json.loads(f.read())
            profiles.append(obj)
    return profiles


async def agent_task(agent: Agent):
    # Start the bot
    agent.start(**SETTINGS["mineflayer_args"])
    await agent.run()
    
    
def runner() -> None:
    print("Getting Profiles")
    profiles = get_profiles()
    print(f'Loading these profiles ${profiles}')
    # Init all agents
    agents: list[Agent] = [Agent(**a) for a in profiles]
    loop = asyncio.new_event_loop()
    for agent in agents:
        loop.create_task(agent_task(agent))
    loop.run_forever()
    

def main():
    try:
        runner()
    except KeyboardInterrupt:
        print("Terminating...")
        return

# Run
if __name__ == "__main__":
    main()