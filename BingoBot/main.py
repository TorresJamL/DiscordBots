import discord
import asyncio
import logging 
import random
import tracemalloc

from discord.ext import commands
from discord import app_commands
from client_ui import FormModal
from game import Game
from game_utils import *

from _t_ import *

tracemalloc.start()

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

#-------------#
#   Globals   #
#-------------#
intents = discord.Intents.all()
client = commands.Bot(command_prefix='--', intents=intents)
curr_guilds = [discord.Object(id = ID) for ID in GUILD_IDS]
game_inst: Game = None

bot_owner = client.owner_id # Manually set this if owner locked items not working

def is_game_active():
    global game_inst
    return bool(game_inst)

async def is_owner(interaction: discord.Interaction):
    if interaction.user.id != bot_owner:
        await interaction.response.send_message(content=f"No Permissions Found for: {interaction.user.name}")  
        return

#--------------------------#
#   Admin Parse Commands   #
#--------------------------#
@client.command(name= "parse")
async def clientside_fib_terminal(ctx: commands.Context, cmd_string:str):
    if (ctx.author.id != bot_owner):
        await ctx.send("`Permissions Invalid.`")
    logging.getLogger(__name__).info()
    collective_output = ""

    await ctx.send(collective_output)

#-----------------------------#
#   Command Implementations   #
#-----------------------------#
async def display_img_impl(interaction: discord.Interaction, view_server_card: bool = False, private:bool = True, user = None):
    """_summary_

    Args:
        interaction (discord.Interaction): _description_
        view_server_card (bool, optional): _description_. Defaults to False.
        private (bool, optional): _description_. Defaults to True.
    """
    if not is_game_active():
        await interaction.response.send_message(content="-# Game session is not active. `start`/`resume` game first.")
        return
    
    global game_inst
    if game_inst.is_setup_phase:
        await interaction.response.send_message(f"Displaying Card Not Possible: In setup phase. Please submit square submissions instead.")
        return
    
    msg_to_weights = {
        "Let's see your progress!" : 100,
        "Sure can do!" : 90,
        "You're ahead of the game! (I did not check)" : 90,
        "Let that sink in. Please. He's cold out there." : 50,
        "Wow." : 70,
        "Programmed it" : 70,
        "-# ***64 times***" : 1,
        "Took a dump, feelin good" : 20,
        "MONKE CITYYYYY" : 20,
        "Here you go!" : 100,
        "You are dumb" : 90,
        "Man." : 65,
    }
    
    target_player = interaction.user.name if not view_server_card else f"{interaction.guild_id}"

    game_inst.create_card_img(target_player)

    msg = random.choices(list(msg_to_weights), list(msg_to_weights.values()), k = 1)[0]

    if not GameData.data_exists(f"CardImgs\\{target_player}_board.png"):
        await interaction.response.send_message(f"No card belonging to, {target_player}, exists.")
        return

    await interaction.response.send_message(
        content=f"{msg}\n"\
                "-# Please note the following\n" \
                "-# - `(0, 0)` is the top left square.\n" \
                "-# - X represents the row #, Y represents the column #. So `(x: 1, y: 2)` is the square 1 row down, 2 columns across.",
        file=discord.File(f"BingoBot\\GameData\\CardImgs\\{target_player}_board.png"), ephemeral=private)
#--------------#
#   Commands   #
#--------------#
@client.tree.command(name="bingo", description="Opens the form.", guilds=curr_guilds)
async def initialize_game(interaction: discord.Interaction):
    global game_inst
    game_inst = Game(interaction.guild_id)
    
    await interaction.response.send_message("```Submission Form Access Granted```")

@client.tree.command(name="advance", description="Generates the Bingo Cards.", guilds=curr_guilds)
async def start_nxt_phase(interaction: discord.Interaction):
    if not is_game_active():
        await interaction.response.send_message(content="-# Game session is not active. `/bingo` game first.")
        return
    global game_inst
    game_inst.is_setup_phase = False
    start_result = game_inst.game_start()
    if not start_result[0]:
        await interaction.response.send_message(content = f"Something went wrong while initializing the game. {start_result[1]}")
        game_inst.is_setup_phase = True
        return
    await interaction.response.send_message(content= "Next phase has begun! Do `/gameplay` to see what to do next. (I am not typing that again)")

@deprecated
@client.tree.command(name="flip_phase", description="[DO NOT USE] Removes access to the submission form and starts the main game.", guilds=curr_guilds)
async def change_game_phase(interaction: discord.Interaction, setup_phase: bool):
    logging.getLogger(__name__).warning("[change_game_phase]: \n\tUnknown Behavior Instigated. Deprecated Function In Use.")
    if not is_game_active() or not is_owner():
        await interaction.response.send_message(content="-# Either Game session is not active or you are not the owner of the bot.")
        return
    global game_inst
    game_inst.is_setup_phase = setup_phase

@client.tree.command(name="info", description="General Information Regarding The Bingo.", guilds=curr_guilds)
async def game_info(interaction: discord.Interaction):
    info = str("""### The following is all information about the BingoBot and how the game works.
1. **MOST IMPORTANT THING** - I can see *EVERYTHING*, you put into the bot. Every submission to the form is saved to a json stored locally on my pc (hidden from the GitHub repo tho), meaning I can (and will) look through it. Due not put any info that only god should know. Hell, don't put anything that only your parents would know. Also, do not submit anything completely unreasonable. This isn't super concerning and mostly applies to random event squares (defined below.) but if I see that someone submits a "Sun blows up" or "President passes" I'm going to "request" (demand) you resubmit.
2. All BingoBot commands are done through slash commands. So, upon typing `/` you should see all available commands usable through this bot. I should have given them all a description so, read.
3. I, Jamil, am not a professional programmer. Do not feel OH-SO~ attached to your card because if something goes wrong and all info is wiped, I most certainly will not heed your whining. Regardless I will attempt to fix it anyways so just send me what your card looked like and I can probs recreate it's data (tediously). Honestly, I'd be the first to whine so don't even.
4. Definitions
> Free Square: A square that should be almost guaranteed to happen.
> Personal Square: A square that is something personal to you, like a goal. 
> Random Square: A random event that you believe to be likely to happen this year. 
> Square: A square on any particular bingo card.
5. Since I made BingoBot, I know how it works pretty well (debatable). If something happens or you need to know how to do smth, ask someone else. I'm not interested.
6. You are welcome to try to break the bot, but please only do this when it first goes up, and not after everyone puts in their data. 
7. By using this bot you are pledging your life to the `Jamil Brand Suite of Products & Merchandise`. Thank you for your contribution.
8. Kill Yourself
`- Jamil`""")
    
    await interaction.response.send_message(info)

@client.tree.command(name="gameplay", description="General Information Regarding The Gameplay.", guilds=curr_guilds)
async def gameplay_info(interaction: discord.Interaction):
    msg = "# Gamplay Description\n" \
    "Gameplay is seperated into two phases:\n" \
    "Setup Phase and the Actual Bingo Stuff TM\n" \
    "### Setup Phase\n" \
    "In the setup phase you can do basically one thing. Using /submit to open the form and enter your square idea." \
    " Note that `personal` squares will only appear on your board and have a small chance of appearing on the server wide card (IDEA IN CONTENTION)." \
    " `free` squares only appear on your own board. `random` squares appear on anyboard (No self-priority system).\n" \
    "There is no set time limit on this phase, as it will continue till every has enough squares which may or may not be programmatically decided.\n" \
    "Only advance to the next stage when everyone is ready. It will not proceed till everyone's (people who submitted) board is full." \
    "### Actual Bingo Stuff TM\n" \
    "Once the setup phase is over (`/advance` being called), you can use `/mark x y` to mark off the square at x,y as done." \
    " The top left square on your card is (0,0) bottom right is (4,4). Going over or under those bounds will not work." \
    " There is no way currently to un-mark a square on the bingo card (working on it [im not]), so preferably do it right first time so I don't need to" \
    "make corrections for you. To see your card, do `/display_card` and it will generate your card. It creates a new image to replace the old one every" \
    " time the commands runs. So problems might occur.\n" \
    "### Server-wide card\n" \
    "The server" \
    "I will update this and normal `/info` as needed. As this bot needs constant surveillance.\n" \
    "`-Jamil`" 

    await interaction.response.send_message(content=msg)

@client.tree.command(name="submit", description="Submit a square for the bingo board.", guilds=curr_guilds)
async def open_modal(interaction: discord.Interaction):
    if not is_game_active():
        await interaction.response.send_message(content="-# Game session is not active. `start`/`resume` game first.")
        return
    global game_inst
    if game_inst.is_setup_phase:
        await interaction.response.send_modal(FormModal())
    else:
        await interaction.response.send_message(content="Game is no longer in setup phase. If you are trying to re-roll your card. DM or ask Jamil, where he'll say no.")

@client.tree.command(name="display_card", description="Display your bingo card (only visible to you)", guilds=curr_guilds)
@app_commands.describe(private = "Whether or not everyone can see your card. (True [meaning yes] by default)", 
                       view_server_card = "If True, displays the server-wide card. Otherwise displays the user's")
async def display_img_cmd(interaction: discord.Interaction, view_server_card: bool = False, private:bool = True):
    await display_img_impl(interaction=interaction, view_server_card=view_server_card, private=private)

@deprecated # THIS COMMAND IS NOT MEANT TO BE USED, ONLY AS A BACKUP
@client.tree.command(name="save", description="Save EVERYTHING manually. (Note: most commands save post result.)", guilds=curr_guilds)
async def manual_save(interaction: discord.Interaction):
    logging.getLogger(__name__).warning("[manual_save] Unknown Behavior Instigated. Deprecated Function In Use.")
    if not is_game_active():
        await interaction.response.send_message(content="-# Game session is not active. `start`/`resume` game first.")
        return
    global game_inst
    try:
        game_inst.save()
    except Exception as err:
        print(err)
        await interaction.response.send_message(content=f"An error occured internally ```{err}```")
    else:
        await interaction.response.send_message(content=f"Done!")
        print("Successful!")

@client.tree.command(name="mark", description="Marks a square on your board @ (x, y) as complete. (0, 0) is the top left square.", guilds=curr_guilds)
@app_commands.describe(x = "Row # starting from 0", y = "Column # starting from 0")
async def mark_square(interaction: discord.Interaction, x:int, y:int):
    if not is_game_active():
        await interaction.response.send_message(content="-# Game session is not active. `start`/`resume` game first.")
        return 
    
    if x > 4 or x < 0 or y > 4 or y < 0:
        await interaction.response.send_message(content="-# Invalid Input. C'mon, you knew that.")
        return
    
    global game_inst
    if game_inst.is_setup_phase:
        await interaction.response.send_message(f"Displaying Card Not Possible: In setup phase. Please submit square submissions instead.")
        return
    
    msg = f"Done! x: {x}, y: {y}, marked!"
    if game_inst.cross_out_sq(interaction.user.name, (x, y)):
        msg += "\nLooks like we gotta a winner?!"

    target_player = interaction.user.name

    game_inst.create_card_img(target_player)

    if not GameData.data_exists(f"CardImgs\\{target_player}_board.png"):
        await interaction.response.send_message(f"No card belonging to, {target_player}, exists.")
        return

    await interaction.response.send_message(
        content=f"{msg}\n"\
                "-# Please note the following\n" \
                "-# - `(0, 0)` is the top left square.\n" \
                "-# - X represents the row #, Y represents the column #. So `(x: 1, y: 2)` is the square 1 row down, 2 columns across.",
        file=discord.File(f"BingoBot\\GameData\\CardImgs\\{target_player}_board.png"), ephemeral=True)

@client.tree.command(name="fibata", description="Create test responses to the form", guilds=curr_guilds)
async def create_test_data(interaction: discord.Interaction, use_real_members:bool = False):
    # *Potential issues located here.
    logging.getLogger(__name__).warning("[create_test_data] Testing Function Proc'ed. Expect issues.")
    if interaction.user.name != "zingiez":
        await interaction.response.send_message(content=f"No Permissions Found for: {interaction.user.name}")  
        return
    try:
        test_people = (["Bob", "Alice", "zingiez", "Prenumbra", "July2026"] if not use_real_members
                       else [member.name for member in interaction.guild.members])
        test_resp_dict = {name: {"Free" : [], "Personal" : [], "Random" : []} for name, v in zip(test_people, [None] * len(test_people))}
        for person in test_people:
            test_resp_dict[person]["Free"] = ["FREE SQUARE"]
            for i in range(50):
                sq_type = random.choice(["Personal", "Random"])
                squ_val = f"{sq_type} | {i} | {person}"
                test_resp_dict[person][sq_type].append(squ_val)

        res = GameData.store_data_to_json(f"{interaction.guild_id}\\form_responses.json", test_resp_dict)
        if not res:
            raise Exception(f"It failed to store. Output: {res}")
    except Exception as err:
        print(err)
    await interaction.response.send_message(content="Done!")  

@client.tree.command(name="get_internal_data", description="Class data", guilds=curr_guilds)
async def get_internal_game_data(interaction: discord.Interaction):
    if interaction.user.name != "zingiez":
        await interaction.response.send_message(content=f"No Permissions Found for: {interaction.user.name}")  
        return
    
    global game_inst
    # logging.getLogger(__name__).info("String of Game Instance: \n" + str(game_inst))

    msg = f"String of Game Instance: \n{str(game_inst)}"
    if len(msg) >= 1990:
        msg = msg[0:1990] + "..."
    msg = "```" + msg + "```"
    await interaction.response.send_message(content=msg)


#-------------------#
#   Client Events   #
#-------------------#
@client.event
async def on_error(event_method, *args, **kwargs):
    logging.getLogger("discord").exception(f"Unhandled exception in {event_method}")
    global game_inst
    logging.getLogger(__name__).warning(str(game_inst))

@client.event
async def on_ready():
    print(f"Bot: {client.user}, online")
    for guild in curr_guilds:
        try:
            await client.tree.sync(guild=guild)
        except discord.errors.Forbidden as forbidden:
            print(f"No access in guild: {repr(guild)}. Error: {forbidden}")


#----------#
#   main   #
#----------#
async def main():
    await client.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
