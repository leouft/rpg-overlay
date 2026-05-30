import json

players = {}
connections = []

async def broadcast_players():

    disconnected = []

    for connection in connections:

        try:

            await connection.send_text(
                json.dumps(players)
            )

        except:

            disconnected.append(connection)

    for connection in disconnected:

        if connection in connections:

            connections.remove(connection)