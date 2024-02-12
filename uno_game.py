import discord
from discord.ext import commands
from discord import app_commands
import random
import math
import player
from player import Player

COLORS = ["red", "green", "blue", "yellow", "wild"]
NORMAL = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "skip", "reverse", "+2", ]
WILDS = ["card", "+4"]

class Deck:
    def __init__(self):
        self.current = genCard()


def genCard():
    col = COLORS[math.floor(random.random() * len(COLORS))]
    if col == "wild":
        return tuple((col, WILDS[math.floor(random.random() * len(WILDS))]))
    else:
        return tuple((col, NORMAL[math.floor(random.random() * len(NORMAL))]))
    

def game(players):
    pass

def getColor(color:str):
    if color == "red":
        return discord.Color.red()
    elif color == "blue":
        return discord.Color.blue()
    elif color == "green":
        return discord.Color.green()
    elif color == "yellow":
        return discord.Color.yellow()
    else:
        return discord.Color.darker_grey()




