from abc import *
from enum import Enum, auto
import market


class BotState(Enum):
    RUN = auto()
    PAUSE = auto()
    STOP = auto()


class Bot(metaclass=ABCMeta):
    def __init__(self, base_asset, init_amount):
        self.base_asset = base_asset
        self.init_amount = init_amount
        self.state = BotState.STOP

    @abstractmethod
    def run(self):
        self.state = BotState.RUN
        market.register_bot(self)

    @abstractmethod
    def pause(self):
        self.state = BotState.PAUSE

    @abstractmethod
    def stop(self):
        self.state = BotState.STOP
        market.remove_bot(self)

    @abstractmethod
    def update(self, market_data):
        pass
