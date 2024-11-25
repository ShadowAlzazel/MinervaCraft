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
    
    
async def start_agents(agents: list[Agent]):
    # Start the agents
    for agent in agents:
        agent.start(**SETTINGS["mineflayer_args"]) # Unpack as kwargs
    # Welcome message
    await agent.send_chat("ShadowAlzazel", "Hello! Welcome to the server")
    
    
async def start() -> None:
    profiles = get_profiles()
    print(f'Loading these profiles ${profiles}')
    agents: list[Agent] = [Agent(**a) for a in profiles]
    await start_agents(agents)
    
    
def runner():
    loop = asyncio.new_event_loop()
    loop.create_task(start())
    loop.run_forever()

def main():
    try:
        #asyncio.run(runner())
        runner()
    except KeyboardInterrupt:
        print("Terminating...")
        return

# Run
if __name__ == "__main__":
    main()