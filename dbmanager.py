import sqlite3

class LocationsManager:
    def __init__(self):
        self.conn = sqlite3.connect('locations.db')
        self.cur = self.conn.cursor()

        self._initialize_structures()
        self._initialize_biomes()
        self._initialize_caves()
        self._initialize_landscapes()
        self._initialize_others()

    def _check_exists(self, name):
        self.cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}'")
        return self.cur.fetchone() is not None

    def _initialize_structures(self):
        if not self._check_exists('Structures'):
            self.cur.execute("""CREATE TABLE Structures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(127),
                x INTEGER NOT NULL,
                y INTEGER DEFAULT NULL,
                z INTEGER NOT NULL,
                explored VARCHAR(31) NOT NULL
            )""")
            self.conn.commit()

    def _initialize_biomes(self):
        if not self._check_exists('Biomes'):
            self.cur.execute("""CREATE TABLE Biomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(127),
                x INTEGER NOT NULL,
                y INTEGER DEFAULT NULL,
                z INTEGER NOT NULL,
                desc VARCHAR(255) NOT NULL
            )""")
            self.conn.commit()

    def _initialize_caves(self):
        if not self._check_exists('Caves'):
            self.cur.execute("""CREATE TABLE Caves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(127),
                x INTEGER NOT NULL,
                y INTEGER DEFAULT NULL,
                z INTEGER NOT NULL,
                size VARCHAR(31) NOT NULL,
                explored VARCHAR(31) NOT NULL
            )""")
            self.conn.commit()

    def _initialize_landscapes(self):
        if not self._check_exists('Landscapes'):
            self.cur.execute("""CREATE TABLE Landscapes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(127),
                x INTEGER NOT NULL,
                y INTEGER DEFAULT NULL,
                z INTEGER NOT NULL,
                beauty INTEGER NOT NULL,
                desc VARCHAR(255) NOT NULL
            )""")
            self.conn.commit()

    def _initialize_others(self):
        if not self._check_exists('Others'):
            self.cur.execute("""CREATE TABLE Others (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(127),
                x INTEGER NOT NULL,
                y INTEGER DEFAULT NULL,
                z INTEGER NOT NULL,
                desc VARCHAR(255) NOT NULL
            )""")
            self.conn.commit()

    def add_location(self, location_dict):
