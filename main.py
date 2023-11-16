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
    if not category:
        await ctx.message.delete()
        await ctx.send("Nenhuma categoria fornecida", delete_after=10)
        return
    if category not in categories.keys():
        await ctx.message.delete()
        await ctx.send("Categoria inválida", delete_after=10)
        return

    locs_ = db.get_locations(categories[category]['name'])
    if not locs_:
        await ctx.message.delete()
        await ctx.send("Nenhuma localização encontrada", delete_after=10)
        return

    msg = ""
    for loc in locs_:
        loc = str(loc).replace("(", "").replace(")", "")
        msg += f"{loc}\n"

    await ctx.send(msg)


@bot.command(name="add")
async def add(ctx, category):
    print(f"{ctx.author} used the add command")
    if category not in categories.keys():
        print(f"{ctx.author} failed to use 'add' with an invalid category")
        await ctx.message.delete()
        await ctx.send("Categoria inválida", delete_after=10)
        return

    categories_ = categories

    def check_author(usr):
        return usr.author == ctx.author

    async def parseinput(inp_str):
        await ctx.send(inp_str)
        var = await bot.wait_for("message", check=check_author)
        return var.content

    name = await parseinput("Digite o nome da sua localização:")
    coords = await parseinput("Digite as coordenadas da sua localização (formato `x y z` com y opcional):")
    args_lst = [name, coords]
    for arg in categories_[category]['args']:
        if arg == 'size':
            arg_inp = await parseinput("Digite o tamanho da caverna:")
        elif arg == 'beauty':
            arg_inp = await parseinput(f"Digite a beleza da paisagem:")
        elif arg == 'explored':
            arg_inp = await parseinput("""Digite a estrutura foi:
            - não explorada
            - parcialmente explorada
            - explorada
            """)
        else:
            arg_inp = await parseinput("Digite uma descrição:")
        args_lst.append(arg_inp)

    class_ = categories_[category]['class']
    loc = class_(*args_lst)

    if db.add_location(loc.as_dict()):
        await ctx.send(f"Localização '{loc.name}' adicionada com sucesso")
    else:
        await ctx.send(f"Erro ao adicionar localização '{loc.name}'")


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
