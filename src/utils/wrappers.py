import asyncio


def RunAsync(fun):
    def wrapper(*args, **kwargs):
        val = asyncio.run(fun(*args, **kwargs))
        return val 
    
    return wrapper