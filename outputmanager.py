from discord import Embed


def _parselocdict(args, values):
    new_dict = {k: v for k, v in zip(args, values)}
    return new_dict


def get_embed_locations(category: str, locs: list, args: list):
    embed = Embed(
        title=f"{category.title()}s",
        description=None,
        color=0x4ad132
    )

    for loc in locs:
        loc_dict = _parselocdict(args, loc)
        name = f"{loc_dict['id']}. {loc_dict['name']}"
        x = loc_dict['x']
        y = loc_dict['y'] if loc_dict['y'] else "~"
        z = loc_dict['z']
        value = f"**Coordenadas:** `{x} {y} {z}`\n"
        if 'explored' in loc_dict.keys():
            value += f"- **{loc_dict['explored'].title()}**\n"
        if 'size' in loc_dict.keys():
            value += f"- **Tamanho:** {loc_dict['size']}\n"
        if 'beauty' in loc_dict.keys():
            value += f"- **Beleza:** {loc_dict['beauty']}\n"
        if 'desc' in loc_dict.keys():
            value += f"- **Descrição:** {loc_dict['desc']}\n"

        embed.add_field(name=name, value=value, inline=False)

    return embed
