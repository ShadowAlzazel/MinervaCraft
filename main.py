import sys
import os 
import json
import asyncio
import multiprocessing

from javascript import require, On, Once

#print("Installing Node Packages...")
require('mineflayer-collectblock')
require('mineflayer-pvp')
require('mineflayer')
#require('minecraft-data')
#require('prismarine-item')
#require('mineflayer-pathfinder')
#
#require('mineflayer-auto-eat')
#require('mineflayer-armor-manager')
#require('mineflayer-tool')

# Main 
from settings import SETTINGS
from src.utils import mf_data
from src.agents.agent import Agent
from src.process import AgentProcess

RUNNING_AGENTS: list[str] = []

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


def thread_task(**profile) -> None:
    agent: Agent = Agent(**profile)
    settings = SETTINGS["minecraft"]
    RUNNING_AGENTS.append(profile["name"])
    process: AgentProcess = AgentProcess(agent, **settings) 
    process.start()


def thread_runner() -> None:
    print(f'Starting Processes...')
    for profile in profiles:
        name = profile["name"]
        # Start a thread for each process agent
        new_process = multiprocessing.Process(target=thread_task(**profile), name=f'{name}-Thread')
        new_process.start()
  
  
  

async def runner() -> None:
    settings = SETTINGS["minecraft"]
    print("Getting Profiles...")
    profiles = get_profiles()
    print(f'Fetched agent profiles.')
    # Init all agents and processes
    agents: list[Agent] = [Agent(**a) for a in profiles]
    processes: list[AgentProcess] = [AgentProcess(a, **settings) for a in agents]
    # Start a task for each agent
    async with asyncio.TaskGroup() as tg:
        for process in processes:
            print(f'Started task for {process.agent.name}')
            tg.create_task(process.start())
 
    
# Main
def main() -> None:
    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        print("Terminating...")
        return


# Run
if __name__ == "__main__":
    main()