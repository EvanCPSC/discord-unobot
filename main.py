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
in_progress = False

def getPlayerByID(id: int):
    for i in range(len(players)):
        if players[i].id == id:
            return players[i]

@client.tree.command(name="join")
async def unogame(interaction: discord.Interaction):
    if not in_progress:
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
        members.remove(interaction.user.id)
        await interaction.response.send_message("Left!", ephemeral=True)
    else:
        await interaction.response.send_message("Already gone!", ephemeral=True)

@client.tree.command(name="start")
async def unogame(interaction: discord.Interaction):
    if not in_progress:
        if len(members) < 2:
            await interaction.response.send_message("Not enough players to start (2 needed)", ephemeral=False)
        elif len(members) == 10:
            await interaction.response.send_message("Player limit reached (10 max)", ephemeral=False)
        else: 
            await interaction.response.send_message("Starting game with " + len(members) + "members...", ephemeral=False)
            in_progress = True
            for i in range(len(members)):
                players.append(Player(members[i]))
    else:
        await interaction.response.send_message("Game has already started!", ephemeral=True)

@client.tree.command(name="end")
async def unogame(interaction: discord.Interaction):
    if in_progress:
        await interaction.response.send_message("Game ended!", ephemeral=False)
        in_progress = False
    else:
        await interaction.response.send_message("There is no game started!", ephemeral=True)

@client.tree.command(name="show_cards")
async def unogame(interaction: discord.Interaction):
    if in_progress:
        playa = getPlayerByID(interaction.user.id)
        await interaction.response.send_message("Your Cards: " + playa.cards, ephemeral=True)
    else:
        await interaction.response.send_message("There is no game started!", ephemeral=True)

client.run(os.getenv("DISCORD_BOT_TOKEN"))