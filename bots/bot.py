from abc import *


class Bot(metaclass=ABCMeta):
    def __init__(self, base_asset, init_amount):
        self.base_asset = base_asset
        self.init_amount = init_amount

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def stop(self):
        pass
