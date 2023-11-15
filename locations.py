class Location:
    """
    A class representing a location in the game.

    Attributes:
    -----------
    name : str
        The name of the location.
    coords : tuple
        The coordinates of the location in the form (x, y, z).
    category : str, optional
        The category of the location.
    size : str, optional
        The size of the location.
    beauty : str, optional
        The beauty of the location.
    explored : str, optional
        Not Explored, Partially Explored or Fully Explored.
    desc : str, optional
        A description of the location.
    """

    def __init__(self, name, coords, category=None, size=None, beauty=None, explored=None, desc=None):
        self.name = name
        self.coords = self._strpcoords(coords)
        self.category = category
        self.desc = desc
        self.size = size
        self.beauty = beauty
        self.explored = explored

    def _strpcoords(self, coords):
        try:
            coords = coords.strip().split()
            coords = [int(coord) for coord in coords]
        except ValueError:
            print(f"Invalid coords for {self.name}")
            return None
        if len(coords) == 2:
            x, z = coords
            y = None
        elif len(coords) == 3:
            x, y, z = coords
        else:
            print(f"Invalid coords for {self.name}")
            return None

        return x, y, z

    def __repr__(self):
        return f"Location '{self.name}' at {self.coords}"

    def as_dict(self):
        """
        Returns a dictionary representation of the location object.
        """
        return {
            'name': self.name,
            'coords': self.coords,
            'category': self.category,
            'size': self.size,
            'beauty': self.beauty,
            'explored': self.explored,
            'desc': self.desc
        }


class Structure(Location):
    """
    Represents a structure in the game world.

    ### Attributes:

    - name (str): the name of the structure.
    - coords (tuple): the coordinates of the structure.
    - category (str): the category of the location (always 'Estrutura' for structures).
    - explored (str): whether the structure is not explored, partially explored or fully explored.
    """

    def __init__(self, name, coords, explored):
        super().__init__(name, coords)
        self.category = 'Structure'
        self.explored = explored

    def __repr__(self):
        return f"Structure '{self.name}' at {self.coords}"


class Biome(Location):
    """
    A class representing a biome in the game world.

    ### Attributes:

    - name (str): the name of the biome
    - coords (tuple): the coordinates of the biome
    - category (str): the category of the location (always 'Bioma' for biomes)
    - desc (str): a description of the biome
    """

    def __init__(self, name, coords, desc):
        super().__init__(name, coords)
        self.category = 'Biome'
        self.desc = desc

    def __repr__(self):
        return f"Biome '{self.name}' at {self.coords}"


class Cave(Location):
    """
    A class representing a cave location in the game.

    ### Attributes:

    - name (str): The name of the cave.
    - coords (tuple): The coordinates of the cave.
    - category (str): The category of the location (always 'Caverna' for caves).
    - size (int): The size of the cave.
    - explored (str): Whether the cave is not explored, partially explored or fully explored.
    """

    def __init__(self, name, coords, size, explored):
        super().__init__(name, coords)
        self.category = 'Cave'
        self.size = size
        self.explored = explored

    def __repr__(self):
        return f"Cave '{self.name}' at {self.coords}"


class Landscape(Location):
    """
    A class representing a landscape location in the game.

    ### Attributes:

    - name (str): The name of the landscape.
    - coords (tuple): The coordinates of the landscape.
    - category (str): The category of the location (always 'Paisagem' for landscapes).
    - beauty (int): The beauty of the landscape (convention is 1-10).
    - desc (str): A description of the landscape.
    """

    def __init__(self, name, coords, beauty, desc):
        super().__init__(name, coords)
        self.category = 'Landscape'
        self.beauty = beauty
        self.desc = desc

    def __repr__(self):
        return f"Landscape '{self.name}' at {self.coords}"


class Other(Location):
    """
    A class representing a location that doesn't fit in any other category.

    ### Attributes:

    - name (str): The name of the location.
    - coords (tuple): The coordinates of the location.
    - category (str): The category of the location (always 'Outro' for other locations).
    - desc (str): A description of the location.
    """

    def __init__(self, name, coords, desc):
        super().__init__(name, coords)
        self.category = 'Other'
        self.desc = desc

    def __repr__(self):
        return f"Other '{self.name}' at {self.coords}"


categories = {
    'estrutura': {'name': 'Structure', 'class': Structure},
    'bioma': {'name': 'Biome', 'class': Biome},
    'caverna': {'name': 'Cave', 'class': Cave},
    'paisagem': {'name': 'Landscape', 'class': Landscape},
    'outro': {'name': 'Other', 'class': Other}
}
