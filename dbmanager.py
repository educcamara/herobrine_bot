import sqlite3


class LocationsManager:
    """Manages the 'locations' database."""

    def __init__(self):
        self.conn = sqlite3.connect('locations.db')
        self.cur = self.conn.cursor()

        self._initialize_locations()

    def _initialize_locations(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Structures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(127),
                    x INTEGER NOT NULL,
                    y INTEGER DEFAULT NULL,
                    z INTEGER NOT NULL,
                    explored VARCHAR(31) NOT NULL
                )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Biomes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(127),
                    x INTEGER NOT NULL,
                    y INTEGER DEFAULT NULL,
                    z INTEGER NOT NULL,
                    desc VARCHAR(255) NOT NULL
                )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Caves (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(127),
                    x INTEGER NOT NULL,
                    y INTEGER DEFAULT NULL,
                    z INTEGER NOT NULL,
                    size VARCHAR(31) NOT NULL,
                    explored VARCHAR(31) NOT NULL
                )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Landscapes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(127),
                    x INTEGER NOT NULL,
                    y INTEGER DEFAULT NULL,
                    z INTEGER NOT NULL,
                    beauty INTEGER NOT NULL,
                    desc VARCHAR(255) NOT NULL
                )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Others (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(127),
                    x INTEGER NOT NULL,
                    y INTEGER DEFAULT NULL,
                    z INTEGER NOT NULL,
                    desc VARCHAR(255) NOT NULL
                )""")
        self.conn.commit()

    @staticmethod
    def _filter_dict(location_dict):
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
        """Adds a location to the database."""
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
            print(f"Failed to add location '{location_dict['name']}' to database")
            print(e)
            return False

    def _count_same_name(self, category, name):
        self.cur.execute(f"SELECT COUNT(*) FROM {category}s WHERE name=?", (name,))
        return self.cur.fetchone()[0]

    def edit_location(self, category, key, value, id_=None, name=None, ) -> int:
        """Edits a location in the database."""
        try:
            if id_:
                self.cur.execute(f"UPDATE {category}s SET {key}=? WHERE id=?", (value, id_))
            elif name:
                if self._count_same_name(category, name) == 0:
                    raise ValueError(f"No location with name '{name}' in {category}s")
                elif self._count_same_name(category, name) > 1:
                    print(f"Failed to edit location '{name}' in {category}s: multiple locations with same name")
                    return 2

                self.cur.execute(f"UPDATE {category}s SET {key}=? WHERE name=?", (value, name))
            else:
                raise ValueError("No name or id provided")

            self.conn.commit()
            print(f"Edited location '{name}' in {category}s: {key}={value}")
            return 0
        except Exception as e:
            print(f"Failed to edit location '{name}' in {category}s: {key}={value}")
            print(e)
            return 1

    def get_locations(self, category):
        """Returns a list of all locations in the database."""
        try:
            self.cur.execute(f"SELECT * FROM {category}s")
        except sqlite3.Error as e:
            print(e)
            return []
        return self.cur.fetchall()

    def get_category_args(self, category):
        """Returns a list of all arguments for the specified category."""
        try:
            self.cur.execute(f"SELECT * FROM {category}s")
        except sqlite3.Error as e:
            print(e)
            return []
        return [description[0] for description in self.cur.description]

    def get_location(self, category, name=None, id_=None):
        """Returns a location with the specified name."""
        try:
            if id_:
                self.cur.execute(f"SELECT * FROM {category}s WHERE id=?", (id_,))
                return [self.cur.fetchone()]
            elif name:
                if self._count_same_name(category, name) == 0:
                    print(f"No location with name '{name}' in {category}s")
                    return []
                elif self._count_same_name(category, name) > 1:
                    print(f"Multiple locations with name '{name}' in {category}s")
                    self.cur.execute(f"SELECT * FROM {category}s WHERE name=?", (name,))
                    return self.cur.fetchall()

                print(f"Found location '{name}' in {category}s")
                self.cur.execute(f"SELECT * FROM {category}s WHERE name=?", (name,))
                return [self.cur.fetchone()]
            else:
                print("No name or id provided")
                return []
        except Exception as e:
            print(f"Failed to get location in {category}s")
            print(e)
            return []

    def delete_location(self, category, id_):
        """Deletes a location with the specified id."""
        try:
            self.cur.execute(f"DELETE FROM {category}s WHERE id=?", (id_,))
            self.conn.commit()
            print(f"Deleted location {id_} from {category}s")
            return True
        except Exception as e:
            print(f"Failed to delete location {id_} from {category}s")
            print(e)
            return False
