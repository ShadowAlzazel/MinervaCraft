import sys
import os 
import json
import asyncio

from javascript import require, On, Once

# Main 
from settings import SETTINGS
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')

# Modules
from src.agents.agent import Agent
from src.process import AgentProcess


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

    
async def runner() -> None:
    print("Getting Profiles...")
    profiles = get_profiles()
    print(f'Fetched agent profiles.')
    # Init all agents
    agents: list[Agent] = [Agent(**a) for a in profiles]
    processes: list[AgentProcess] = [AgentProcess(a) for a in agents]
    # Start a task for each agent
    #loop = asyncio.new_event_loop()
    #for agent in agents:
    #    loop.create_task(agent_task(agent))
    #loop.run_forever()
    async with asyncio.TaskGroup() as task_group:
        for process in processes:
            process.start_bot(**SETTINGS["mineflayer_args"])
            task_group.create_task(process.agent_task())
    
    
def main():
    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        print("Terminating...")
        return

# Run
if __name__ == "__main__":
    main()