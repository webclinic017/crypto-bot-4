import market
from time import sleep
from bots.test_bot import TestBot


def main():
    market.init()
    bot = TestBot('btcusdt', 100)
    bot.run()
    sleep(100)
    bot.stop()
    market.close()


if __name__ == "__main__":
    main()
