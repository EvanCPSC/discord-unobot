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
    
def formCard(card: tuple):
    return str.upper(card[0][0]) + card[0][1::] + " " + card[1]
    
def formHand(hand):
    re = ""
    for card in hand:
        re += formCard(card) + ", "
    return re[0:-2]

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
    description="/join : Joins the game (before starting)\n"
    + "/leave : Leaves the game (before starting)\n"
    + "/start : Starts a game if there is none going on (2-10 Players)\n"
    + "/end : Ends the game if there is one going on\n"
    + "/hand : Shows your cards in your hand\n"
    + "/place : Place a card down (use \'newcolor\' if placing a wild)\n"
    + "/draw : Draw a card to your hand\n"
    + "/rules : Sends the rules and commands via direct message"
)

RULES = discord.Embed(
    color=discord.Color.blurple(),
    title="Rules of Uno!Bot:",
    description="Setup:\n2-10 players, each player gets 7 cards.\nThe first person to join will be the first to go.\n\n"
    + "Gameplay:\n On your turn, either:\n- Place a card that matches the current card's color or value\n- Place a wild card\n"
    + "  - (If game starts with a wild, any color can be chosen)\n"
    + "- Draw a card (1 per turn)\n- First player to zero cards wins!\n\n"
    + "Special Cards:\n- Reverse: Inverts the turn order.\n- Skip: Skip the next player's turn (no stacking).\n"
    + "- +2 (Draw Two): Next player must draw 2 cards and skip their turn (no stacking).\n\n"
    + "Wild Cards:\n- Wild Card: use the \'newcolor\' variable to change the color.\n"
    + "- +4 (Draw Four): Next player must draw 4 cards and skip their turn (no stacking). "
    + "Also changes color using the \'newcolor\' variable.\n\n"
)

