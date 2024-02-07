import interactions
import os
from dotenv import load_dotenv

load_dotenv()
bot = interactions.Client(token=os.getenv("DISCORD_BOT_TOKEN"),
    default_scope=os.getenv("GUILD_SCOPE"),)

@interactions.slash_command(
    name="my_first_command",
    description="This is the first command I made!",
)
async def my_first_command(ctx: interactions.ComponentContext):
    await ctx.send("Hi there!")

bot.start()
