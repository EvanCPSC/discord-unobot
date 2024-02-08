import discord
from discord.ext import commands
from discord import app_commands
class Player:
    def __init__(self, member):
        self.id = member # member is interaction.user.id