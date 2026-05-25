from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
import json, unicodedata
from fastapi.responses import FileResponse

# Função pra pegar essa disgrama de nome sem ficar com acento nem os carai
def create_player_id(name):

    normalized = unicodedata.normalize("NFD", name)

    no_accents = "".join(

        char for char in normalized

        if unicodedata.category(char) != "Mn"

    )

    return (
        no_accents
        .strip()
        .lower()
        .replace(" ", "_")
    )

app = FastAPI()

app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)

players = {}

connections = []

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
                "hp": data["hp"],
                "maxHp": data["maxHp"],

                "mental": data["mental"],
                "maxMental": data["maxMental"],

                "energy": data["energy"]
            }

            print(players)

            for connection in connections:

                await connection.send_text(
                    json.dumps(players)
                )

    except:
        connections.remove(websocket)