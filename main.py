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
    print(f'{client.user} is running.')
    try:
        synced = await client.tree.sync()
        print(f'Synced {len(synced)} tree commands.')
    except Exception as e:
        print(f'Could Not Sync Tree: {e}')

members = []
players = []
global in_progress
in_progress = False
global currCard
global turn
global rev
rev = 1


@client.tree.command(name="join", description="Joins the game (before starting)")
async def unogame(interaction: discord.Interaction):
    if not inProgress():
        if interaction.user not in members:
            members.append(interaction.user)
            await interaction.response.send_message("<@" + str(interaction.user.id) + "> has joined! [" + str(len(members)) + "/10]")
        else:
            await interaction.response.send_message("Already in the game!", ephemeral=True) 
    else:
        await interaction.response.send_message("Game has already started!", ephemeral=True)

@client.tree.command(name="leave", description="Leaves the game (before starting)")
async def unogame(interaction: discord.Interaction):
    if not inProgress():
        if interaction.user in members:
            members.remove(interaction.user)
            await interaction.response.send_message("<@" + str(interaction.user.id) + "> has left! [" + str(len(members)) + "/10]")
        else:
            await interaction.response.send_message("Already gone!", ephemeral=True)
    else:
        if len(players) > 2:
            removedTurn = members.index(interaction.user)
            players.remove(getPlayerByID(interaction.user))
            members.remove(interaction.user)
            if turn == removedTurn:
                updateTurnLeave()
                await interaction.response.send_message(content="<@" + str(interaction.user.id) + "> has left! [" + str(len(members)) + "/10]\n" + "<@" + str(players[turn].mem.id) + ">'s turn!", embed=discord.Embed(color=uno_game.getColor(currCard[0]), title='Current Card:', description=uno_game.formCard(currCard)), ephemeral=False)
            else:
                await interaction.response.send_message("<@" + str(interaction.user.id) + "> has left! [" + str(len(members)) + "/10]")
        else:
            await interaction.response.send_message("<@" + str(interaction.user.id) + "> has left! Not enough players to continue game. Game ended!")
            endGame()

@client.tree.command(name="start", description="Starts a game if there is none going on (2-10 Players)")
async def unogame(interaction: discord.Interaction):
    if not inProgress():
        lMem = len(members)
        if lMem < 2:
            await interaction.response.send_message("Not enough players to start (2 needed)", ephemeral=False)
        elif lMem == 10:
            await interaction.response.send_message("Player limit reached (10 max)", ephemeral=False)
        else: 
            startGame()
            for i in range(len(members)):
                players.append(Player(members[i]))
            await interaction.response.send_message(content="Starting game with " + str(lMem) + " members...\n<@" + str(players[0].mem.id) + ">'s turn!", embed=discord.Embed(color=uno_game.getColor(currCard[0]), title='Current Card:', description=uno_game.formCard(currCard)), ephemeral=False)
            
    else:
        await interaction.response.send_message("Game has already started!", ephemeral=True)

@client.tree.command(name="end", description="Ends the game if there is one going on")
async def unogame(interaction: discord.Interaction):
    if inProgress():
        if interaction.user in members:
            await interaction.response.send_message("Game ended!", ephemeral=False)
            endGame()
        else:
            await interaction.response.send_message("Your not in the game! meanie.", ephemeral=True)
    else:
        await interaction.response.send_message("There is no game started!", ephemeral=True)

@client.tree.command(name="hand", description="Shows your cards in your hand")
async def unogame(interaction: discord.Interaction):
    if inProgress():
        playa = getPlayerByID(interaction.user)
        await interaction.response.send_message("Your Cards: " + uno_game.formHand(playa.cards), ephemeral=True)
    else:
        await interaction.response.send_message("There is no game started!", ephemeral=True)

@client.tree.command(name="place", description="Place a card down (use \'newcolor\' if placing a wild)")
@discord.app_commands.describe(
    color='Red, Green, Blue, Yellow, or Wild',
    value='Normal: 0-9, Skip, Reverse, +2 or Wild: Card, +4',
    newcolor='Red, Green, Blue, or Yellow if placing a Wild'
)
async def unogame(interaction: discord.Interaction,
                  color: str,
                  value: str,
                  newcolor:str = ""
                  ):
    if turn == members.index(interaction.user):
        if inProgress():
            playa = getPlayerByID(interaction.user)
            color = color.lower()
            value = value.lower()
            newcolor = newcolor.lower()
            for i in range(len(playa.cards)):
                if color == playa.cards[i][0] and value == playa.cards[i][1]:
                    if color == currCard[0] or color == "wild" or value == currCard[1] or currCard[0] == "wild":
                        if color == "wild":
                            if uno_game.getColor(newcolor) != None:
                                color = newcolor
                            else:
                                await interaction.response.send_message("Not a valid color!", ephemeral=True)
                                break
                        changeCard(color, value)
                        analyzeValue(value)
                        playa.cards.pop(i)
                        if not playa.cards:
                            await interaction.response.send_message("<@" + str(players[turn-rev].mem.id) + "> puts down " + uno_game.formCard(currCard) + " and wins!", ephemeral=False)
                            endGame()
                        else:
                            await interaction.response.send_message(content="<@" + str(players[turn].mem.id) + ">'s turn!", embed=discord.Embed(color=uno_game.getColor(currCard[0]), title='Current Card:', description=uno_game.formCard(currCard)), ephemeral=False)
                        break
                    else:
                        await interaction.response.send_message("That card doesn't match!", ephemeral=True)
                elif i + 1 == len(playa.cards):
                    await interaction.response.send_message("You don't have that card!", ephemeral=True)
                    break
        else:
            await interaction.response.send_message("There is no game started!", ephemeral=True)
    else:
        await interaction.response.send_message("It's not your turn!", ephemeral=True)

@client.tree.command(name="draw", description="Draw a card to your hand")
async def unogame(interaction: discord.Interaction):
    if turn == members.index(interaction.user):
        if inProgress():
            playa = getPlayerByID(interaction.user)
            card = uno_game.genCard()
            playa.cards.append(card)
            analyzeValue("")
            channel = interaction.channel
            await channel.send("<@" + str(players[turn-rev].mem.id) + "> drew!\n<@" + str(players[turn].mem.id) + ">'s turn!")
            await interaction.response.send_message("You drew a " + uno_game.formCard(card) + "!", ephemeral=True)
        else:
            await interaction.response.send_message("There is no game started!", ephemeral=True)
    else:
        await interaction.response.send_message("It's not your turn!", ephemeral=True)

@client.tree.command(name="rules", description="Sends the rules and commands via direct message")
async def unogame(interaction: discord.Interaction):
    await interaction.user.send(embed=uno_game.COMMANDS)
    await interaction.user.send(embed=uno_game.RULES)
    await interaction.response.send_message("Rules and Commands sent!", ephemeral=True)

def analyzeValue(value:str):
    global turn
    global rev
    match value:
        case "skip":
            turn = (turn + (2*rev)) % len(players)
        case "+2":
            turn = (turn + rev) % len(players)
            players[turn].cards.extend([uno_game.genCard() for i in range(2)])
            turn = (turn + rev) % len(players)
        case "+4":
            turn = (turn + rev) % len(players)
            players[turn].cards.extend([uno_game.genCard() for i in range(4)])
            turn = (turn + rev) % len(players)
        case "reverse":
            rev *= -1
            two_players = True if len(players) == 2 else False
            turn = (turn + rev + two_players) % len(players)
        case _:
            turn = (turn + rev) % len(players)

def updateTurnLeave():
    global turn
    turn = (turn + rev) % len(players) if rev == -1 else turn % len(players)

def inProgress():
    global in_progress
    return in_progress

def changeState():
    global in_progress
    in_progress = not in_progress

def changeCard(color:str, value:str):
    global currCard
    currCard = tuple((color, value))

def getPlayerByID(user: discord.User):
    for i in range(len(players)):
        if players[i].mem.id == user.id:
            return players[i]
        
def endGame():
    global members
    global players
    members = []
    players = []
    global turn
    turn = 0
    changeState()

def startGame():
    global currCard
    currCard = uno_game.genCard()
    global turn
    turn = 0
    changeState()


client.run(os.getenv("DISCORD_BOT_TOKEN"))