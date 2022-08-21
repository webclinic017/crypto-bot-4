import market
from time import sleep


def main():
    market.init()
    sleep(10)
    market.close()


if __name__ == "__main__":
    main()