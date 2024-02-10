import os
from dotenv import load_dotenv

load_dotenv()

import discord
from discord.ext import commands
from discord import app_commands
import uno_game
import player
from player import Player

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Set all permissions for discord bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Set bot prefix as slash
client = commands.Bot(command_prefix='/', intents=intents)


@client.event # listener
async def on_ready():
    print(F'{client.user} is running.')
    try:
        synced = await client.tree.sync()
        print(F'Synced {len(synced)} tree commands.')
    except Exception as e:
        print(F'Could Not Sync Tree: {e}')

members = []
players = []
global in_progress
in_progress = False
global currCard

def inProgress():
    global in_progress
    return in_progress

def changeState():
    global in_progress
    in_progress = not in_progress

def getPlayerByID(id: int):
    for i in range(len(players)):
        if players[i].id == id:
            return players[i]
        
def endGame():
    global members
    global players
    members = []
    players = []

def startGame():
    global currCard
    currCard = discord.Embed(color=discord.Color.blurple(), title='Current Card:', description=uno_game.genCard())

@client.tree.command(name="join")
async def unogame(interaction: discord.Interaction):
    if not inProgress():
        if interaction.user.id not in members:
            members.append(interaction.user.id)
            await interaction.response.send_message("Joined!", ephemeral=True)
        else:
            await interaction.response.send_message("Already in the game!", ephemeral=True) 
    else:
        await interaction.response.send_message("Game has already started!", ephemeral=True)

@client.tree.command(name="leave")
async def unogame(interaction: discord.Interaction):
        if interaction.user.id in members:
            players.remove(getPlayerByID(interaction.user.id))
            members.remove(interaction.user.id)
            await interaction.response.send_message("Left!", ephemeral=True)
        else:
            await interaction.response.send_message("Already gone!", ephemeral=True)

@client.tree.command(name="start")
async def unogame(interaction: discord.Interaction):
    if not inProgress():
        lMem = len(members)
        if lMem < 2:
            await interaction.response.send_message("Not enough players to start (2 needed)", ephemeral=False)
        elif lMem == 10:
            await interaction.response.send_message("Player limit reached (10 max)", ephemeral=False)
        else: 
            startGame()
            await interaction.response.send_message(content="Starting game with " + str(lMem) + " members...", embed=currCard, ephemeral=False)
            changeState()
            for i in range(len(members)):
                players.append(Player(members[i]))
    else:
        await interaction.response.send_message("Game has already started!", ephemeral=True)

@client.tree.command(name="end")
async def unogame(interaction: discord.Interaction):
    if inProgress():
        await interaction.response.send_message("Game ended!", ephemeral=False)
        changeState()
        endGame()
    else:
        await interaction.response.send_message("There is no game started!", ephemeral=True)

@client.tree.command(name="show_cards")
async def unogame(interaction: discord.Interaction):
    if inProgress():
        playa = getPlayerByID(interaction.user.id)
        await interaction.response.send_message("Your Cards: " + str(playa.cards), ephemeral=True)
    else:
        await interaction.response.send_message("There is no game started!", ephemeral=True)

@client.tree.command(name="place")
@discord.app_commands.describe(
    
)
async def unogame(interaction: discord.Interaction,
                  color: str,
                  value: str
                  ):
    if inProgress():
        playa = getPlayerByID(interaction.user.id)
        await interaction.response.send_message("Your Cards: " + str(playa.cards), ephemeral=True)
    else:
        await interaction.response.send_message("There is no game started!", ephemeral=True)

client.run(os.getenv("DISCORD_BOT_TOKEN"))