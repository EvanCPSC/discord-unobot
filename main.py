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

def changeCard(color:str, value:str):
    global currCard
    currCard = tuple((color, value))

def getPlayerByID(id: int):
    for i in range(len(players)):
        if players[i].id == id:
            return players[i]
        
def endGame():
    global members
    global players
    members = []
    players = []
    changeState()

def startGame():
    global currCard
    currCard = uno_game.genCard()
    changeState()

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
            await interaction.response.send_message(content="Starting game with " + str(lMem) + " members...", embed=discord.Embed(color=uno_game.getColor(currCard[0]), title='Current Card:', description=currCard), ephemeral=False)
            for i in range(len(members)):
                players.append(Player(members[i]))
    else:
        await interaction.response.send_message("Game has already started!", ephemeral=True)

@client.tree.command(name="end")
async def unogame(interaction: discord.Interaction):
    if inProgress():
        await interaction.response.send_message("Game ended!", ephemeral=False)
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

@client.tree.command(name="place", description="Place a card down")
@discord.app_commands.describe(
    color='Red, Green, Blue, Yellow, or Wild',
    value='Normal: 0-9, Skip, Reverse, +2 or Wild: Card, +4'
)
async def unogame(interaction: discord.Interaction,
                  color: str,
                  value: str
                  ):
    if inProgress():
        playa = getPlayerByID(interaction.user.id)
        for i in range(len(playa.cards)):
            if color.lower() == playa.cards[i][0] and value.lower() == playa.cards[i][1]:
                if color.lower() == currCard[0] or color.lower() == "wild" or value.lower() == currCard[1]:
                    changeCard(color, value)
                    await interaction.response.send_message(embed=discord.Embed(color=uno_game.getColor(currCard[0]), title='Current Card:', description=currCard), ephemeral=False)
                    playa.cards.pop(i)
                    break
                else:
                    await interaction.response.send_message("That card doesn't match!", ephemeral=True)
            elif i + 1 == len(playa.cards):
                await interaction.response.send_message("You don't have that card!", ephemeral=True)
                break
        
    else:
        await interaction.response.send_message("There is no game started!", ephemeral=True)

@client.tree.command(name="draw")
async def unogame(interaction: discord.Interaction):
    if not inProgress():
        playa = getPlayerByID(interaction.user.id)
        card = uno_game.genCard()
        playa.cards.append(card)
        await interaction.response.send_message("You drew a " + str(card) + "!", ephemeral=True)
    else:
        await interaction.response.send_message("There is no game started!", ephemeral=True)

client.run(os.getenv("DISCORD_BOT_TOKEN"))