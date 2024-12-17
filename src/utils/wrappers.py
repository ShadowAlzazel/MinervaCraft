import asyncio

from javascript import On, Once, AsyncTask, start, stop, abort

"""
async def Listener(func):
    
    async def wrapper(*args, **kwargs):
        task = asyncio.create_task(func(*args, **kwargs))
        result = await task
        return result
    return await wrapper 

"""

"""
def Listener(func):
    async def wrapper(*args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            # Await the coroutine if the function is async
            return await func(*args, **kwargs)
        else:
            # Call the sync function directly
            return func(*args, **kwargs)
    return wrapper

"""