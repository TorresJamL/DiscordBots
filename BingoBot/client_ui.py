import discord
import logging
import json

from pathlib import Path
from game_utils import GameData
from discord.ext import commands
from discord.ui.media_gallery import *
from discord.ui import Select, Modal, Label
from discord import *

class FormModal(Modal):
    def __init__(self):
        super().__init__(title="2026 Bingo Form.")
        text_inp_component = discord.ui.TextInput(
            style=TextStyle.long,
            placeholder="Enter Something IDK here"
        )
        menu_select_component = Select(
            placeholder="Square Type",
            min_values=1,
            max_values=1,
            options=[
                SelectOption(
                    label="Free",
                    description="The middle square on the bingo card. SHOULD BE EASY!"
                ), SelectOption(
                    label="Personal",
                    description="This means your square is a personal goal for 2026. Guaranteed to be on your own board."
                ), SelectOption(
                    label="Random",
                    description="Any event that might happen in 2026. SHOULD BE POSSIBLE."
                ),
            ]
        )
        self.add_item(Label(
            text="What would you like to have on ",
            component=text_inp_component))
        
        self.add_item(Label(
            text="What kind of Square is it?",
            description="descri",
            component=menu_select_component))

    async def callback(self, interaction: Interaction):
        print("Start of callback")
        await interaction.response.send_message(content="Im so tired", ephemeral=True)
        print("called backed")

    async def on_submit(self, interaction: Interaction):
        await interaction.response.send_message(
            "Modal submitted successfully!",
            ephemeral=True
        )
        
        response_dict, form_resp_path = GameData.get_data_from_json(f"{interaction.guild_id}\\form_responses.json")

        user = interaction.user.name
        if response_dict.get(user) == None:
            response_dict[user] = {
                "Free" : [],
                "Personal" : [],
                "Random" : []
            }
        square_type = self.children[1].component.values[0]
        square_value = str(self.children[0].component)
        response_dict[user][square_type].append(square_value)

        with open(form_resp_path, 'w+') as responses_json:
            json.dump(response_dict, responses_json, indent=4)
        
    async def on_error(self, interaction: Interaction, error):
        logging.getLogger("discord").error(f"Error in modal {self}: {error}", exc_info=error)
