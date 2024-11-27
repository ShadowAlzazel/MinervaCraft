import asyncio

from javascript import require, On, Once

def RunAsync(fun):
    def wrapper(*args, **kwargs):
        val = asyncio.run(fun(*args, **kwargs))
        return val 
    
    return wrapper