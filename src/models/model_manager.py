from ..models import gpt

def find_model(api: str, model: str):
    match api:
        case "gpt":
            return gpt.GPT
        case _:
            return None
        
        
def get_model_args(**profile):
    match profile["api"]:
        case "gpt":
            return {
                "instructions": profile["conversing"],
                "name": profile["name"],
                "model": profile["model"],
                "temperature": profile.get("temperature", 1.0),
                "api": profile["api"]
            }
        case _:
            return None