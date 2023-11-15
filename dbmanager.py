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

    def _initialize_structures(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Structures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(127),
            x INTEGER NOT NULL,
            y INTEGER DEFAULT NULL,
            z INTEGER NOT NULL,
            explored VARCHAR(31) NOT NULL
        )""")
        self.conn.commit()

    def _initialize_biomes(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Biomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(127),
            x INTEGER NOT NULL,
            y INTEGER DEFAULT NULL,
            z INTEGER NOT NULL,
            desc VARCHAR(255) NOT NULL
        )""")
        self.conn.commit()

    def _initialize_caves(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Caves (
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
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Landscapes (
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
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Others (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(127),
            x INTEGER NOT NULL,
            y INTEGER DEFAULT NULL,
            z INTEGER NOT NULL,
            desc VARCHAR(255) NOT NULL
        )""")
        self.conn.commit()

    def _filter_dict(self, location_dict):
        keys = []
        new_dct = {}
        for key, value in location_dict.items():
            if key == 'coords':
                keys += ['x', 'y', 'z']
                new_dct['x'], new_dct['y'], new_dct['z'] = value
            elif key == 'category':
                pass
            elif value is not None:
                keys.append(key)
                new_dct[key] = value
        
        return keys, new_dct

    def add_location(self, location_dict) -> bool:
        try:
            table_name = location_dict['category'] + 's'
            keys, location_dict = self._filter_dict(location_dict)
            keys_str = '(' + ', '.join(keys) + ')'
            values = tuple(location_dict.values())
            values_str = '(' + ', '.join(['?'] * len(values)) + ')'

            self.cur.execute(f"INSERT INTO {table_name} {keys_str} VALUES {values_str}", values)

            self.conn.commit()
            print(f"Added location '{location_dict['name']}' to {table_name}")
            return True
        except Exception as e:
            print(f"Failed to add location '{location_dict['name']}' to {table_name}")
            print(e)
            return False

    def edit_location(self, category, name, key, value) -> bool:
        try:
            table_name = category + 's'

            self.cur.execute(f"UPDATE {table_name} SET {key}=? WHERE name=?", (value, name))

            self.conn.commit()
            print(f"Edited location '{name}' in {table_name}: {key}={value}")
            return True
        except Exception as e:
            print(f"Failed to edit location '{name}' in {table_name}: {key}={value}")
            print(e)
            return False
    
    def get_locations(self, category):
        self.cur.execute(f"SELECT * FROM {category}s")
        return self.cur.fetchall()
    
    def get_location(self, category, name):
        self.cur.execute(f"SELECT * FROM {category}s WHERE name=?", (name,))
        return self.cur.fetchone()
