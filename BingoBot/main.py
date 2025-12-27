import discord
import asyncio
import logging 
import tracemalloc
import json

from discord.ext import commands
from form import FormModal
from _t_ import TOKEN, GUILD_ID
from bingo import BingoCard, CardSquare
from pathlib import Path

tracemalloc.start()

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

intents = discord.Intents.all()
client = commands.Bot(command_prefix='-', intents=intents)
test_guild = discord.Object(id = GUILD_ID)

class Game:
    def __init__(self):
        self.free_squares = {}
        self.personal_squares = {}
        self.random_squares = []
    
    def game_start(self):
        pass

    def load_square_data(self):
        curr_file_dir = Path(__file__).resolve().parent
        form_resp_path = curr_file_dir / "GameData/form_responses.json"
        
        if not Path(form_resp_path).exists():
            with open(form_resp_path, 'w+') as responses_json:
                json.dump(dict(), responses_json, indent=4)

        with open(form_resp_path, 'r') as responses_json:
            response_dict:dict = json.load(responses_json)

        

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