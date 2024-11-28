from ..models import gpt, llama

def find_model(api: str, model: str):
    match api:
        case "gpt":
            return gpt.GPT 
        case "llama":
            return llama.LLama
        case _:
            return None
        
        
def get_model_args(**profile):
    api = profile["api"]
    if api == "gpt" or api == "llama":
        return {
            "instructions": profile["conversing"],
            "name": profile["name"],
            "model": profile["model"],
            "temperature": profile.get("temperature", 0.7),
            "api": profile["api"]
        }
    else:
        return None 
    