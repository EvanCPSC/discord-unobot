import discord
from discord.ext import commands
from discord import app_commands
import uno_game
class Player:
    def __init__(self, member):
        self.id = member # member is interaction.user.id
        self.cards = []

    def genCards(self):
        for i in range(7):
            self.cards.append(uno_game.genCard())