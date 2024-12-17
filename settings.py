SETTINGS = {
    "minecraft": {
        "version": "1.21.1", # The minecraft version
        "host": "localhost", # or "127.0.0.1", "localhost", "host.docker.internal"
        "port": 25568, # Docker/Proxy -> 25568, Direct -> 55916
        "auth": "microsoft", # or "offline"
    },

    "profiles": [
        #"minerva",
        #"freya",
        #"ophelia"
        #"himiko",
        "vail",
    ],

    "load_memory": False, # load memory from previous session
    "language": "en",
    "skills_on": True, # Whether to have actions and skills be called
}