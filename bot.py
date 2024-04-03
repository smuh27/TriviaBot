import discord, os, requests, html
from discord.ui import Select, View, Button
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
GUILD_ID = int(os.getenv('GUILD_TOKEN'))
CHANNEL_ID = int(os.getenv('CHANNEL_TOKEN'))
API_KEY = os.getenv('API_KEY')
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='$', intents=intents)

random = requests.get('https://opentdb.com/api.php?amount=1&type=boolean').json()
# mythology = requests.get('https://opentdb.com/api.php?amount=1&category=20&type=boolean').json()

# correct_myth_answer = mythology['results'][0]['correct_answer']
correct_answer = random['results'][0]['correct_answer']


user_answer = ""
player = ""


class buttonView(discord.ui.View):
    @discord.ui.button(label="True")
    async def true_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_answer = "True"
        if (user_answer == correct_answer):
            await interaction.response.send_message("Correct")
        else:
             await interaction.response.send_message("Incorrect")
    @discord.ui.button(label="False")
    async def false_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_answer = "False"
        if (user_answer == correct_answer):
            await interaction.response.send_message("Correct")
        else:
             await interaction.response.send_message("Incorrect")


class MyView(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose a Category", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Any",
                description="Click for Any!"
            ),
            discord.SelectOption(
                label="Mythology",
                description="Click for Mythology!"
            )
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select): # the function called when the user is done selecting options
        view = buttonView()
        embed = discord.Embed (
            color=discord.Color.random(),
        )
        embed.set_author(name=player)
        if (select.values[0] == 'Any'):
            embed.add_field(name="Question", value=html.unescape(random['results'][0]['question']))
        
        await interaction.response.send_message(embed=embed , view=view)

    

@client.command()
async def Trivia(ctx):
    global player
    player = ctx.author.name
    await ctx.send("Choose a Category", view=MyView())


       
client.run(TOKEN)