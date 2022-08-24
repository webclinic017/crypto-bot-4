from fastapi import FastAPI
from fastapi.websockets import WebSocket
from bots.test_bot import TestBot
from fastapi.testclient import TestClient
from time import  sleep

app = FastAPI()


@app.get("/")
def read_root():
    test_websocket()
    return {"Hello": "World"}


@app.websocket_route("/ws")
async def websocket(websocket: WebSocket):
    bot = TestBot('btcusdt', 100)
    bot.run()
    await websocket.accept()
    while True:
        sleep(1)
        await websocket.send_json({"msg": bot.roe})


def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        for i in range(10):
            data = websocket.receive_json()
            print(data)
