from aiogram.utils.token import TokenValidationError
import pytest

from os import getenv
from interruptingcow import timeout

from tnotify import Bot


@pytest.mark.asyncio
async def test_init_with_wrong_token():
    with pytest.raises(TokenValidationError):
        bot = Bot("random text")
        bot.stop_polling()
    
@pytest.mark.asyncio
async def test_init_with_correct_token():
    token = getenv('TG_BOT_TOKEN')
    
    bot = Bot(token)
    bot.stop_polling()

@pytest.mark.asyncio
async def test_start_polling_correct_token():
    token = getenv('TG_BOT_TOKEN')
    
    class TimeoutEx(Exception): pass
    
    bot = None
    
    try:
        with timeout(5., exception=TimeoutEx):
            bot = Bot(token)
            bot.start_polling()
            while True:
                pass
    except TimeoutEx:
        bot.stop_polling()
        assert True
    
