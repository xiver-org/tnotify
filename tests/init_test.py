import asyncio
import sys
from aiogram.utils.token import TokenValidationError
import pytest

from os import getenv
from interruptingcow import timeout

from tnotify import Bot


@pytest.mark.asyncio
async def test_init_with_wrong_token():
    with pytest.raises(TokenValidationError):
        Bot("random text")
    
@pytest.mark.asyncio
async def test_init_with_correct_token():
    token = getenv('TG_BOT_TOKEN')
    
    Bot(token)

@pytest.mark.asyncio
async def test_start_polling_correct_token():
    token = getenv('TG_BOT_TOKEN')
    
    class TimeoutEx(Exception): pass
    
    try:
        with timeout(5., exception=TimeoutEx):
            Bot(token).start_polling()
            while True:
                pass
    except TimeoutEx:
        assert True
    
