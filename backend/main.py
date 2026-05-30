from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
import asyncio, json
from fastapi.responses import FileResponse
from backend.state import (
    players,
    connections,
    broadcast_players
)
from backend.utils import create_player_id
from backend.bot import start_bot

app = FastAPI()

@app.on_event("startup")
async def startup_event():

    asyncio.create_task(
        start_bot()
    )

app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)

# Vê se tá online
@app.get("/")
def home():
    return {"status": "online"}

# Acessa painel de player
@app.get("/player")
def player():
    return FileResponse("frontend/player.html")

# Acessa o overlay por usuário overlay/nome_do_usuario
@app.get("/overlay/{player_name}")
def overlay(player_name: str):
    return FileResponse("frontend/overlay.html")

# man
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    connections.append(websocket)

    await websocket.send_text(
        json.dumps(players)
    )

    try:

        while True:

            message = await websocket.receive_text()

            data = json.loads(message)

            player_id = create_player_id(data["player"])      

            players[player_id] = {
                "displayName": data["player"],
                "peCurrent": data["peCurrent"],
                "peMax": data["peMax"],

                "knockout": data["knockout"],

                "courage": data["courage"]
            }

            print(players)

            await broadcast_players()

    except:
        connections.remove(websocket)