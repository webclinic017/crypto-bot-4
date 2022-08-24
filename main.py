import market
from time import sleep
from bots.test_bot import TestBot
import uvicorn
import asyncio

import user_api


def main():
    market.init()
    uvicorn.run("user_api:app", host="0.0.0.0", port=8000)
    """
    bot = TestBot('btcusdt', 100)
    bot.run()
    sleep(100)
    bot.stop()
    market.close()
    """


if __name__ == "__main__":
    main()
