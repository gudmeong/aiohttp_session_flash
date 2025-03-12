"""
Session flash messages for aiohttp.web
"""

import asyncio
from functools import partial, wraps

from aiohttp_session import get_session

SESSION_KEY = REQUEST_KEY = 'flash'

def async_wrapper(func):
    @wraps(func)
    
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)
    
    return wrapper

def flash(request, message):
	  request[REQUEST_KEY].append(message)


def pop_flash(request):
	  flash = request[REQUEST_KEY]
	  request[REQUEST_KEY] = []
	  return flash


@async_wrapper
def middleware(app, handler):
    @async_wrapper
	  def process(request):
		    session = yield from get_session(request)
    		flash_incoming = session.get(SESSION_KEY, [])
    		request[REQUEST_KEY] = flash_incoming[:]  # copy flash for modification
		
    		try:
    			  response = yield from handler(request)
    		finally:
    			  flash_outgoing = request[REQUEST_KEY]
    			  if flash_outgoing != flash_incoming:
    				    if flash_outgoing:
    					      session[SESSION_KEY] = flash_outgoing
    				else:
    					  del session[SESSION_KEY]
    		
    		return response

	  return process


@async_wrapper
def context_processor(request):
	  return {
	  	'get_flashed_messages': partial(pop_flash, request),
	  }
