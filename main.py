import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from inputmanager import *

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=">", intents=intents)


categories = {
    "estrutura": ["nome", "coordenadas"],
    "bioma": ["nome", "coordenadas"],
    "paisagem": ["nome", "coordenadas", "descrição"],
    "caverna": [
        "nome",
        "coordenadas",
        "tamanho",
    ],
    "outro": ["nome", "coordenadas", "descrição"],
}


@bot.event
async def on_ready():
    print(f"\033[32m{bot.user} logged in as {bot.user.name}\033[0m")


@bot.command(name="ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    print(f"{ctx.author} used the ping command ({latency}ms)")
    await ctx.send(f"Pong com {latency}ms")


@bot.command(name="add")
async def add(ctx, category):
    if category not in categories:
        await ctx.send(
            f"""Não existe a categoria '{category}'
                       Para saber como funciona o comando `add`, digite `>help add`"""
        )
        print("command 'add' failed by INVALID_CATEGORY")
        return

    def check(usr):
        return usr.author == ctx.author and usr.channel == ctx.channel

    await ctx.send(f"Digite o nome da localização de categoria **{category}**")
    msg = await bot.wait_for("message", check=check)
    name = msg.content
    await ctx.send(f'Digite as coordenadas de "{name}"')

    return


load_dotenv()
token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
