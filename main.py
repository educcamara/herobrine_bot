import os
import discord
from discord.ui import Button, View
from discord.ext import commands
from dotenv import load_dotenv
from locations import *
from dbmanager import *

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=">", intents=intents)
db = LocationsManager()

@bot.event
async def on_ready():
    print(f"\033[32m{bot.user} logged in as {bot.user.name}\033[0m")


@bot.command(name="ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    print(f"{ctx.author} used the ping command ({latency}ms)")
    await ctx.send(f"Pong com {latency}ms")


@bot.command(name="locs")
async def locs(ctx, category):
    print(f"{ctx.author} used the locs command")
    if category not in categories.keys():
        await ctx.message.delete()
        await ctx.send("Categoria inválida", delete_after=10)
        return

    locs_ = db.get_locations(categories[category])
    if not locs_:
        await ctx.message.delete()
        await ctx.send("Nenhuma localização encontrada", delete_after=10)
        return

    msg = ""
    for loc in locs_:
        loc_ = str(*loc)
        msg += f"{loc_}\n"

    await ctx.send(msg)


@bot.command(name="add")
async def add(ctx, category):
    print(f"{ctx.author} used the add command")
    if category not in categories.keys():
        await ctx.message.delete()
        await ctx.send("Categoria inválida", delete_after=10)
        return




@bot.command(name="ephemeral")
async def ephemeral(ctx):
    print(f"{ctx.author} used the ephemeral command")
    button = Button(label="Cadu", style=discord.ButtonStyle.primary)

    view = View()
    view.add_item(button)
    msg = await ctx.send("Sarve", view=view)

    async def callback(interaction):
        await interaction.response.send_message(content="Salve senhor", ephemeral=True)
        await ctx.message.delete()
        await msg.delete()

    button.callback = callback


load_dotenv()
token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
