import asyncio
from aiogram.utils.token import TokenValidationError
import pytest

import importlib
from os import getenv
import threading

import tnotify

@pytest.mark.asyncio
async def test_init_with_wrong_token():
    with pytest.raises(TokenValidationError):
        bot = tnotify.Bot("random text")
        bot.stop_polling()
    
@pytest.mark.asyncio
async def test_init_with_correct_token():
    token = getenv('TG_BOT_TOKEN')
    
    bot = tnotify.Bot(token)
    bot.stop_polling()

@pytest.mark.asyncio
async def test_start_polling_correct_token():
    token = getenv('TG_BOT_TOKEN')
    
    loop = asyncio.new_event_loop()
    bot = tnotify.Bot(token)
    
    def __check():
        asyncio.set_event_loop(loop)
        
        bot.start_polling()
        while True:
            pass
    
    thread = threading.Thread(target=__check)
    thread.daemon = True
    thread.start()

    thread.join(5)

    if thread.is_alive():
        bot.stop_polling()
        loop.stop()        
        assert True
    else:
        loop.stop()
        assert False
    
