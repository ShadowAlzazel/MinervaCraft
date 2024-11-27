from openai import OpenAI
from typing import Optional, Union

from ..utils import keys

class GPT:
    
    def __init__(self, **kwargs):
        # Start a client
        self.name: str = kwargs["name"]
        new_key = keys.get_key("OPENAI_API_KEY")
        client = OpenAI(
            api_key=new_key
        )
        self.client = client
        self.api: str = kwargs["api"]
        self.model: str = kwargs["model"]
        # Load in tools
        model_tools = self._create_tools(kwargs["commands"])
        # Start the assistant
        #self.assistant = client.beta.assistants.create(
        #    instructions=kwargs["instructions"],
        #    name=kwargs["name"],
        #    tools=model_tools, # Get From commands
        #    model=kwargs["model"],
        #    temperature=kwargs["temperature"]
        #)
        self.instructions: str = kwargs["instructions"]
        self.temperature = kwargs["temperature"]
        self.tools = model_tools 
        print(f'[{self.name}] Loaded new client ({self.api}) with the model ({self.model})')
      
    # Other models may have different notation
    def _create_tools(self, commands: list):
        tools = []
        for x in commands:
            tool_obj = {
                "type": "function",
                "function": x
            }
            tools.append(tool_obj)
        return tools
        
    
    async def send_request(self, message: str, role: str="user", context: Optional[list]=None):
        messages = []
        if context:
            messages = context
        messages.append({"role": role, "content": message})
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            tools=self.tools
        )
        response = completion.choices[0].message
        print(f'Response Choice: {response}')
        return response
    
    
    async def send_prompt(self, message: str, context: Optional[list]=None):
        response = await self.send_request(message, "user", context)
        return response