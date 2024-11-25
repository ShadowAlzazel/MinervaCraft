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
                "tools": profile["skills"],
            }
        case _:
            return None