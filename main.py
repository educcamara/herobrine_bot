import os
import discord
from discord.ui import Button, View
from discord.ext import commands
from dotenv import load_dotenv
from locations import *
from dbmanager import *
from outputmanager import *

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


async def getinput(ctx, inp_str) -> str:
    await ctx.send(inp_str)
    var = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
    return var.content


async def checkcategory(ctx, category: str):
    if not category:
        await ctx.message.delete()
        await ctx.send("Nenhuma categoria fornecida", delete_after=10)
        return False
    if category not in categories.keys():
        await ctx.message.delete()
        await ctx.send("Categoria inválida", delete_after=10)
        return False
    return True


async def sendlocations(ctx, category: str):
    cat_name = categories[category]['name']
    locs_ = db.get_locations(cat_name)
    if not locs_:
        await ctx.message.delete()
        await ctx.send(f"Nenhuma localização da categoria '{category}' encontrada", delete_after=10)
        return
    args_ = db.get_category_args(cat_name)
    embed = get_embed_locations(category, locs_, args_)

    await ctx.send(embed=embed)


@bot.command(name="locate")
async def locate(ctx, category: str):
    print(f"{ctx.author} used the locs command")
    if not await checkcategory(ctx, category):
        return

    await sendlocations(ctx, category)


@bot.command(name="add")
async def add(ctx, category: str):
    print(f"{ctx.author} used the add command")
    if not await checkcategory(ctx, category):
        return

    categories_ = categories

    name = await getinput(ctx, "Digite o nome da sua localização:")
    coords = await getinput(ctx, "Digite as coordenadas da sua localização (formato `x y z` com y opcional):")
    args_lst = [name, coords]
    for arg in categories_[category]['args']:
        if arg == 'size':
            arg_inp = await getinput(ctx, "Digite o tamanho da caverna:")
        elif arg == 'beauty':
            arg_inp = await getinput(ctx, f"Digite a beleza da paisagem:")
        elif arg == 'explored':
            arg_inp = await getinput(ctx, "Digite se a estrutura foi:\n\
                                          - **Explorada**\n\
                                          - **Parcialmente explorada**\n\
                                          - **Não explorada**\n")
            arg_inp = arg_inp.title()
        else:
            arg_inp = await getinput(ctx, "Digite uma descrição:")
        args_lst.append(arg_inp)

    class_ = categories_[category]['class']
    loc = class_(*args_lst)

    if db.add_location(loc.as_dict()):
        await ctx.send(f"Localização '{loc.name}' adicionada com sucesso")
    else:
        await ctx.send(f"Erro ao adicionar localização '{loc.name}'")


@bot.command(name="edit")
async def edit(ctx, category: str):
    print(f"{ctx.author} used the edit command")
    if not await checkcategory(ctx, category):
        return

    await sendlocations(ctx, category)
    categories_ = categories
    cat_name = categories_[category]['name']

    id_ = await getinput(ctx, "Digite o ID da localização que deseja editar:")
    if not id_.isdigit():
        await ctx.message.delete()
        await ctx.send("ID inválido", delete_after=10)
        return

    if not db.get_location(cat_name, id_=id_):
        await ctx.message.delete()
        await ctx.send(f"Localização de ID {id_} não encontrada", delete_after=10)
        return

    key_value = await getinput(ctx, "Digite o nome do atributo (nome, coordenadas, exploração, \
tamanho, beleza, descrição) que deseja editar e seu novo valor (formato `atributo valor`):")
    try:
        key_value = key_value.split()
        key = key_value[0]
        key_translator = {
            'nome': 'name',
            'coordenadas': 'coords',
            'exploração': 'explored',
            'tamanho': 'size',
            'beleza': 'beauty',
            'descrição': 'desc'
        }
        if key not in key_translator.keys():
            await ctx.message.delete()
            await ctx.send("Atributo inválido", delete_after=10)
            return
        key = key_translator[key]
        if key == 'coords':
            coords = key_value[1:]
            if len(coords) == 2:
                x, z = [int(coord) for coord in coords]
                y = None
            elif len(coords) == 3:
                x, y, z = [int(coord) for coord in coords]
            else:
                await ctx.message.delete()
                await ctx.send("Coordenadas inválidas", delete_after=10)
                return
            db.edit_location(cat_name, 'x', x, id_=id_)
            db.edit_location(cat_name, 'y', y, id_=id_)
            db.edit_location(cat_name, 'z', z, id_=id_)
        elif key == 'beauty':
            beauty = int(key_value[1])
            db.edit_location(cat_name, key, beauty, id_=id_)
        else:
            value = ' '.join(key_value[1:])
            db.edit_location(cat_name, key, value, id_=id_)
    except Exception as e:
        await ctx.message.delete()
        await ctx.send("Erro ao editar localização", delete_after=10)
        print(e)
        return
    await ctx.send(f"Localização de ID {id_} editada com sucesso")


@bot.command(name="delete")
async def delete(ctx, category: str):
    print(f"{ctx.author} used the delete command")
    if not await checkcategory(ctx, category):
        return

    await sendlocations(ctx, category)
    categories_ = categories
    cat_name = categories_[category]['name']

    id_ = await getinput(ctx, "Digite o ID da localização que deseja deletar:")
    if not id_.isdigit():
        await ctx.message.delete()
        await ctx.send("ID inválido", delete_after=10)
        return

    if db.delete_location(cat_name, id_):
        await ctx.send(f"{category.title()} de ID {id_} deletado(a) com sucesso")
    else:
        await ctx.send(f"Erro ao deletar localização de ID {id_} em '{category}'")


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
