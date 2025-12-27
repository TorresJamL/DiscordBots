import discord
import logging
import json

from pathlib import Path
from game_utils import GameData

class FormModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="2026 Bingo Form.")
        text_inp_component = discord.ui.TextInput(
            style=discord.TextStyle.long,
            placeholder="Enter Something IDK here"
        )
        menu_select_component = discord.ui.Select(
            placeholder="Square Type",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(
                    label="Free",
                    description="The middle square on the bingo card. SHOULD BE EASY!"
                ), discord.SelectOption(
                    label="Personal",
                    description="This means your square is a personal goal for 2026. Guaranteed to be on your own board."
                ), discord.SelectOption(
                    label="Random",
                    description="Any event that might happen in 2026. SHOULD BE POSSIBLE."
                ),
            ]
        )
        self.add_item(discord.ui.Label(
            text="What would you like to have on ",
            component=text_inp_component))
        
        self.add_item(discord.ui.Label(
            text="What kind of Square is it?",
            description="descri",
            component=menu_select_component))

    async def callback(self, interaction: discord.Interaction):
        print("Start of callback")
        await interaction.response.send_message(content="Im so tired", ephemeral=True)
        print("called backed")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Modal submitted successfully!",
            ephemeral=True
        )
        
        response_dict, form_resp_path = GameData.get_data_from_json("form_responses.json")

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
        
    async def on_error(self, interaction, error):
        logging.getLogger("discord").error(f"Error in modal {self}: {error}", exc_info=error)