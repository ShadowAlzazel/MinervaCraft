import ollama

from typing import Optional, Union

from ..utils import keys

class LLama:
    
    def __init__(self, **kwargs):
        # Start a client
        self.name: str = kwargs["name"]
        new_key = keys.get_key("OPENAI_API_KEY")
        client = ollama.Client(
            host="http://localhost:11434"
        )
        self.client = client
        self.api: str = kwargs["api"]
        self.model: str = kwargs["model"]
        # Load in tools
        model_tools = self._create_tools(kwargs["commands"])
        self.tools = model_tools 
        # Parameters
        self.instructions: str = kwargs["instructions"]
        self.temperature = kwargs["temperature"]
        # Run
        
      
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
        options = {
            "temperature": self.temperature
        }
        response = self.client.chat(
            model=self.model,
            messages=messages,
            options=options,
            tools=self.tools
        )
        chat = response.message
        print(f'Response Choice: {chat}')
        return chat
    
    
    async def send_prompt(self, message: str, context: Optional[list]=None):
        # Create history and memory manager
        history = []
        # Use searching to find a conversation/history from the context
        messages = []
        if not context:
            messages = [{"role": "system", "content": self.instructions}]
        else:
            messages = context
        response = await self.send_request(message, "user", messages)
        return response