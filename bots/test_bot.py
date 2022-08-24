from bots.bot import *


class TestBot(Bot):
    def __init__(self, base_asset, init_amount):
        super().__init__(base_asset, init_amount)
        self.entry_price = -1
        self.roe = 0

    def run(self):
        super().run()

    def pause(self):
        super().pause()

    def stop(self):
        super().stop()

    def update(self, market_data):
        super().update(market_data)

        cur = market_data[self.base_asset][market.INTERVAL_1DAY][market.KLINE_CLOSE][-1]

        if self.entry_price == -1:
            self.entry_price = market_data[self.base_asset][market.INTERVAL_1DAY][market.KLINE_CLOSE][-1]
        else:
            self.roe = round(((cur - self.entry_price) / self.entry_price) * 100, 2)

        # print(f'entry: {self.entry_price}, cur: {cur}, roe: {self.roe}')
