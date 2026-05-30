import discord
from discord.ext import commands
from dotenv import load_dotenv
from backend.state import (
    players,
    connections,
    broadcast_players
)
from backend.utils import create_player_id

import os

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

CHANNEL_ID = os.getenv("DISCORD_CHANNEL")

intents = discord.Intents.all()

intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,

    max_messages=10000
)

def parse_sheet(content):

    lines = content.splitlines()

    return {
        "displayName":
            lines[0],
        "peCurrent":
            int(lines[1].split(":")[1]),
        "peMax":
            int(lines[2].split(":")[1]),
        "knockout":
            int(lines[3].split(":")[1]),
        "courage":
            int(lines[4].split(":")[1]),
    }

async def process_sheet(message):

    data = parse_sheet(
        message.content
    )

    player_id = create_player_id(
        data["displayName"]
    )

    players[player_id] = data

    print(players)

    await broadcast_players()

@bot.event
async def on_ready():

    print(
        f"Bot conectado como {bot.user}"
    )

    channel = bot.get_channel(CHANNEL_ID)

    async for message in channel.history(limit=100):

        bot._connection._messages.append(message)

        try:

            await process_sheet(
                message
            )

        except Exception as e:

            print(
                f"Erro ao processar a mensagem: {e}"
            )

@bot.event
async def on_message_edit(before, after):

    try:

        await process_sheet(after)

    except Exception as e:

        print(
            f"Erro ao editar ficha: {e}"
        )

@bot.event
async def on_message(message):

    if message.author.bot:
        return
    
    if message.channel.id != CHANNEL_ID:
        return
    
    try:
        await process_sheet(message)

    except Exception:
        pass

async def start_bot():

    await bot.start(TOKEN)