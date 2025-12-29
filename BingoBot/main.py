import discord
import asyncio
import logging 
import tracemalloc
import json

from discord.ext import commands
from form import FormModal
from bingo import BingoCard, CardSquare
from game_utils import GameData
from game import Game
from pathlib import Path
from _t_ import TOKEN, GUILD_ID

tracemalloc.start()

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

intents = discord.Intents.all()
client = commands.Bot(command_prefix='--', intents=intents)
test_guild = discord.Object(id = GUILD_ID)

#--------------#
#   Commands   #
#--------------#
@client.command(name="bingo")
async def begin_game(ctx: commands.Context):
    guild = ctx.guild
    user_invoker = ctx.author
    inst = Game()
    await ctx.send("Starting game...")

@client.tree.command(name="open_form", description="Submit a square for the bingo board.", guild=test_guild)
async def open_modal(interaction: discord.Interaction):
    await interaction.response.send_modal(FormModal())

@client.event
async def on_error(event_method, *args, **kwargs):
    logging.getLogger("discord").exception(f"Unhandled exception in {event_method}")

@client.event
async def on_ready():
    print(f"Bot: {client.user}, online")
    await client.tree.sync(guild=test_guild)

async def main():
    inst = Game()
    inst.load_square_data()
    inst.print_data()
    await client.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
