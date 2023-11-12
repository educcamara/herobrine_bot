import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=">", intents=intents)


categories = {
    'estrutura': None,
    'bioma': None,
    'paisagem': None,
    'caverna': None,
    'outro': None
}


@bot.event
async def on_ready():
    print(f"\033[32m{bot.user} logged in as {bot.user.name}\033[0m")


@bot.command(name='ping')
async def ping(ctx):
    latency = round(bot.latency * 1000)
    print(f"{ctx.author} used the ping command ({latency}ms)")
    await ctx.send(f"Pong com {latency}ms")


@bot.command(name='add')
async def add(ctx, category):
    return


load_dotenv()
token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
