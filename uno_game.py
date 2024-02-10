import discord
from discord.ext import commands
from discord import app_commands
import random
import math
import player
from player import Player

COLORS = ["Red", "Green", "Blue", "Yellow", "Wild"]
NORMAL = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "+2", ]
WILDS = ["Card", "+4"]

class Deck:
    def __init__(self):
        self.current = genCard()


def genCard():
    col = COLORS[math.floor(random.random() * len(COLORS))]
    if col == "Wild":
        return tuple((col, WILDS[math.floor(random.random() * len(WILDS))]))
    else:
        return tuple((col, NORMAL[math.floor(random.random() * len(NORMAL))]))
    

def game(players):
    pass




