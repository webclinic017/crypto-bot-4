from bots.bot import *


class TestBot(Bot):
    def __init__(self, base_asset, init_amount):
        super().__init__(base_asset, init_amount)

    def run(self):
        super().run()

    def pause(self):
        super().pause()

    def stop(self):
        super().stop()

    def update(self, market_data):
        super().update(market_data)
        print(market_data[self.base_asset][market.INDICATOR_SMA7][-1])
