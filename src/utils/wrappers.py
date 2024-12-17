import asyncio

from javascript import require, On, Once

#async def AsyncRun(fun):
#    async def wrapper(*args, **kwargs):
#        task = asyncio.create_task(fun(*args, **kwargs))
#        return await task 
#    return await wrapper

# Create task group manager

#def TrackFun(fun):
#    def wrapper(*args, **kwargs):
#       val = fun(*args, **kwargs)
#        print(f'The function {fun} was called!')
#        return val 
    
#    return wrapper


def Listener(fun):
    # Create a task
    async def _task(*args, **kwargs):
        task = asyncio.create_task(fun(*args, **kwargs))
        return await task 

    def _wrapper(*args, **kwargs):
        asyncio.run(_task(*args, **kwargs))    
    
    return _wrapper