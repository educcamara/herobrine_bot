def strpcoords(coords: str):
    coords = coords.strip().split()
    if len(coords) == 2:
        try:
            x = int(coords[0])
            z = int(coords[1])
            y = '~'
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
