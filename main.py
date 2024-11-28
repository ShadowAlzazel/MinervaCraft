import sys
import os 
import json
import asyncio

from javascript import require, On, Once

# Main 
from settings import SETTINGS
from src.utils import mcdata
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
    # Init all agents and processes
    agents: list[Agent] = [Agent(**a) for a in profiles]
    processes: list[AgentProcess] = [AgentProcess(a) for a in agents]
    # Start a task for each agent
    async with asyncio.TaskGroup() as task_group:
        for process in processes:
            process.start_bot(**SETTINGS["start_args"])
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