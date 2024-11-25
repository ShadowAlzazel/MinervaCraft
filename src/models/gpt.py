from openai import OpenAI

from ..utils import keys

class GPT:
    
    def __init__(self, **kwargs):
        # Start a client
        new_key = keys.get_key("OPENAI_API_KEY")
        client = OpenAI(
            api_key=new_key
        )
        self.client = client
        self.model = kwargs["model"]
        # Start the assistant
        self.assistant = client.beta.assistants.create(
            instructions=kwargs["instructions"],
            name=kwargs["name"],
            tools=kwargs["tools"], # Get From skills
            model=kwargs["model"],
        )
        
    
    async def get_completion(self, messages: list[dict]):
        # Conversations via threads
        #response = await self.client.beta.threads.create(
        #    
        #)
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return completion
    
    
    async def get_message(self, messages: list[dict]):
        completion = await self.get_completion(messages)
        return completion.choices[0].message