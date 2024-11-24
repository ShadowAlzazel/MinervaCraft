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


def getProfiles() -> list[dict]:
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
    
    
def main():
    profiles = getProfiles()
    print(f'Loading these profiles ${profiles}')
    agents: list[Agent] = [Agent(a["name"]) for a in profiles]
    # Run
    for agent in agents:
        agent.start(**SETTINGS["kwargs"]) # Unpack as kwargs

    active = True
    while active:
        pass

# Run
if __name__ == "__main__":
    main()