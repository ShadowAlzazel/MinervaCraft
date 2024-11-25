import json

KEYS = {}

def load_keys():
    global KEYS
    file_path = "keys.json"
    # Load KEYS obj with API secrets
    with open(file_path, "r") as f:
        obj = json.loads(f.read())
        for key, value in obj.items():
            if not value:
                continue
            KEYS[key] = value


def get_key(key: str) -> str:
    load_keys()
    return KEYS[key]