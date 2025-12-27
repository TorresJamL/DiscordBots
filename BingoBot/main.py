import discord
import asyncio
import logging 
import tracemalloc
import json

from discord.ext import commands
from form import FormModal
from bingo import BingoCard, CardSquare
from game_utils import GameData
from pathlib import Path
from _t_ import TOKEN, GUILD_ID

tracemalloc.start()

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

intents = discord.Intents.all()
client = commands.Bot(command_prefix='-', intents=intents)
test_guild = discord.Object(id = GUILD_ID)

class Game:
    __active_sessions = {} # {sesh_id : data_directory, ...}
    
    def __init__(self):
        self.sesh_id = 0
        self.sesh_data_dir = ""

        self.free_squares: dict[str, list] = {}
        self.personal_squares: dict[str, list] = {}
        self.random_squares = []

        self.player_to_card: dict[str, BingoCard] = {}
    
    def game_start(self):
        pass

    def save(self):
        pass
    
    @staticmethod
    def postsave(func):
        def wrapper():
            func()
        return wrapper
    
    @staticmethod
    def add_game_session(id:int, data_directory:str):
        pass
    
    def load_square_data(self):
        response_dict = GameData.get_data_from_json("form_responses.json")[0]

    def load_game_data(self):
        pass


        

#--------------#
#   Commands   #
#--------------#
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
    await client.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())