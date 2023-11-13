"""
This module contains functions to get user input
"""
from discord.ui import View, Button, ButtonStyle

def _strpcoords(coords: str):
    """
    Parses coordinates from string
    """
    coords = coords.strip().split()
    if len(coords) == 2:
        try:
            x = int(coords[0])
            z = int(coords[1])
            y = "~"
        except ValueError:
            return None
    elif len(coords) == 3:
        try:
            x = int(coords[0])
            y = int(coords[1])
            z = int(coords[2])
        except ValueError:
            return None
    else:
        return None

    return f"{x} {y} {z}"


async def getcoords(ctx, bot, name: str):
    """
    Gets coordinates from user
    """
    def _check(usr):
        return usr.author == ctx.author and usr.channel == ctx.channel

    await ctx.send(f'Digite as coordenadas de "{name}"')
    msg = await bot.wait_for("message", check=_check)
    coords = _strpcoords(msg.content)
    if not coords:
        await ctx.send("Coordenadas inválidas")
        return None

    return coords


async def getdesc(ctx, bot, name: str):
    """
    Gets description from user
    """
    def _check(usr):
        return usr.author == ctx.author and usr.channel == ctx.channel

    await ctx.send(f'Digite a descrição de "{name}"')
    msg = await bot.wait_for("message", check=_check)
    desc = msg.content
    if not desc:
        await ctx.send("Descrição inválida")
        return None

    return desc


async def getsize(ctx, bot, name: str):
    """"
    Gets 'caverna' size from user
    """
    def _check(usr):
        return usr.author == ctx.author and usr.channel == ctx.channel

    await ctx.send(f'Digite o tamanho da caverna "{name}"')
    msg = await bot.wait_for("message", check=_check)
    size = msg.content
    if not size:
        await ctx.send("Tamanho inválido")
        return None

    return size


async def getbeauty(ctx, bot, name: str):
    """
    Gets 'paisagem' beauty score from user
    """
    def _check(usr):
        return usr.author == ctx.author and usr.channel == ctx.channel

    await ctx.send(f'Digite a beleza da paisagem "{name}"')
    msg = await bot.wait_for("message", check=_check)
    beauty = msg.content
    if not beauty:
        await ctx.send("Beleza inválida")
        return None

    return beauty


async def getexploration(ctx, name: str):
    """
    Gets Exploration status from user
    """
    def _check(usr):
        return usr.author == ctx.author and usr.channel == ctx.channel

    await ctx.send(f'Selecione o status de exploração de "{name}":')

    view = View()
    view.add_item(Button(style=ButtonStyle.grey,
                         label="Não Explorado",
                         custom_id="not_explored"))
    view.add_item(Button(style=ButtonStyle.blurple,
                         label="Ainda Explorando",
                         custom_id="exploring"))
    view.add_item(Button(style=ButtonStyle.green,
                         label="Já Explorado",
                         custom_id="explored"))

    interaction = await view.wait()
    exploration = interaction.component.label

    return exploration
