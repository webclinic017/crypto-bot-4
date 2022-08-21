from binance.um_futures import UMFutures
import numpy as np
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
import os, certifi, win32api
from talipp.indicators import SMA

# CONSTANTS
KLINE_OPEN = 'open'
KLINE_HIGH = 'high'
KLINE_LOW = 'low'
KLINE_CLOSE = 'close'
KLINE_VOLUME = 'volume'
KLINE_TIME = 'time'

INTERVAL_1MINUTE = '1m'
INTERVAL_1DAY = '1d'

INDICATOR_SMA7 = 'sma7'


# GLOBAL VARIABLES
symbols = ['btcusdt']
intervals = [INTERVAL_1MINUTE, INTERVAL_1DAY]
window_size = 50

"""
market_data {
    'symbol': {
        'interval': {
            ohlcvt values...
        }, ... ,
        'indicator': {
        }, ....
    }, ...
}
"""
market_data = {}

client = UMFutures()
ws_client = UMFuturesWebsocketClient()


def kline_handler(msg):
    s = msg['data']['s'].lower()  # symbol이 대문자로 옴
    kline = msg['data']['k']
    i = kline['i']
    t = str(kline['t'])  # int to str

    if t == market_data[s][i][KLINE_TIME][-1]:
        for key in market_data[s][i]:
            if key != KLINE_TIME:
                market_data[s][i][key][-1] = float(kline[key[0]])

        if i == INTERVAL_1DAY:
            market_data[s][INDICATOR_SMA7].update_input_value(float(kline[KLINE_CLOSE[0]]))
    else:
        print(s + ' ' + i + ' ' + t + ' ' + market_data[s][i][KLINE_TIME][-1])
        print(market_data[s][i])

        for key in market_data[s][i]:
            market_data[s][i][key] = np.delete(market_data[s][i][key], 0)
            if key != KLINE_TIME:
                market_data[s][i][key] = np.append(market_data[s][i][key], float(kline[key[0]]))
            else:
                market_data[s][i][key] = np.append(market_data[s][i][key], t)

        print(market_data[s][i])

        if i == INTERVAL_1DAY:
            market_data[s][INDICATOR_SMA7].purge_oldest(1)
            market_data[s][INDICATOR_SMA7].add_input_value(float(kline['c']))

    print(market_data[s][INDICATOR_SMA7][-1])


def init():
    os.environ['SSL_CERT_FILE'] = certifi.where()
    ws_client.start()

    stream = []
    # init market_data
    for s in symbols:
        market_data[s] = {}
        for i in intervals:
            market_data[s][i] = {}
            stream.append(s + '@kline_' + i)

            tmp = np.array(client.klines(symbol=s, interval=i, limit=window_size))
            market_data[s][i][KLINE_OPEN] = tmp[:, 1].astype(float)
            market_data[s][i][KLINE_HIGH] = tmp[:, 2].astype(float)
            market_data[s][i][KLINE_LOW] = tmp[:, 3].astype(float)
            market_data[s][i][KLINE_CLOSE] = tmp[:, 4].astype(float)
            market_data[s][i][KLINE_VOLUME] = tmp[:, 5].astype(float)
            market_data[s][i][KLINE_TIME] = tmp[:, 0]

        market_data[s][INDICATOR_SMA7] = SMA(period=7, input_values=market_data[s][INTERVAL_1DAY][KLINE_CLOSE])

    ws_client.instant_subscribe(
        stream=stream,
        callback=kline_handler,
    )


def close():
    win32api.SetConsoleCtrlHandler(lambda _: ws_client.stop(), True)
    # ws_client.stop()
