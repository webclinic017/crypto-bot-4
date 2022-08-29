from fastapi import FastAPI
from fastapi.websockets import WebSocket

import market
from bots.test_bot import TestBot
from fastapi.testclient import TestClient
from time import sleep

app = FastAPI()


@app.get("/")
def read_root():
    # test_websocket()
    return {"Hello": "World"}


@app.get("/create/")
async def create_bot(amount: int = 100):
    bot = TestBot('btcusdt', amount)
    bot.run()
    print("bot enrolled")
    return {"Create": "Bot"}


@app.websocket_route("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        sleep(1)
        ret = []
        for bot in market.enrolled_bots:
            ret.append(bot.roe)
        await websocket.send_json({"roes": ret})


def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        for i in range(10):
            data = websocket.receive_json()
            print(data)
