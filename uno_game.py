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
        return None


COMMANDS = discord.Embed(
    color=discord.Color.blurple(),
    title="Commands:",
    description=""
)

RULES = discord.Embed(
    color=discord.Color.blurple(),
    title="Rules of Uno!Bot:",
    description="Setup:\n2-10 players, each player gets 7 cards.\nThe first person to join will be the first to go.\n\n"
    + "Gameplay:\n On your turn, either:\n- Place a card that matches the current card's color or value\n- Place a wild card\n"
    + "- Draw a card (1 per turn)\n- First player to zero cards wins!\n\n"
    + "Special Cards:\n- Reverse: Inverts the turn order.\n- Skip: Skip the next player's turn (no stacking).\n"
    + "- +2 (Draw Two): Next player must draw 2 cards and skip their turn (no stacking).\n\n"
    + "Wild Cards:\n- Wild Card: use the \'new_color\' variable to change the color.\n"
    + "- +4 (Draw Four): Next player must draw 4 cards and skip their turn (no stacking). "
    + "Also can change color using the \'new_color\' variable.\n\n"
)

