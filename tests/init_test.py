import asyncio
import time
from aiogram.utils.token import TokenValidationError
import pytest

import importlib
from os import getenv
import threading

import tnotify

@pytest.mark.asyncio
async def test_init_with_wrong_token():
    with pytest.raises(TokenValidationError):
        bot = tnotify.Bot("random text", log_level='TRACE')
        bot.stop_polling()
    
def test_init_with_correct_token():
    token = getenv('TG_BOT_TOKEN')
    
    bot = tnotify.Bot(token, log_level='TRACE')
    bot.stop_polling()


def test_start_polling_correct_token():
    token = getenv('TG_BOT_TOKEN')

    bot = tnotify.Bot(token, log_level='TRACE')
    
    bot.start_polling()
    iters = 0
    while iters < 5:
        time.sleep(1)
        iters += 1
        
    bot.stop_polling()
    assert True


def test_restart_polling():
    token = getenv('TG_BOT_TOKEN')

    bot = tnotify.Bot(token, log_level='TRACE')
    
    bot.start_polling()
    bot.stop_polling()
    bot.start_polling()
