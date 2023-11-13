import sqlite3


class SQLManager:
    """
    A class to manage SQLite database for Minecraft world exploration data.
    """
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.categories = {
            'estrutura': {'name': 'Estruturas', 
                          'args': ['nome', 'coordenadas', 'explorada'], 
                          'str_args': '(nome, coordenadas, explorada) VALUES (?, ?, ?)'},
            'bioma': {'name': 'Biomas', 
                      'args': ['nome', 'coordenadas', 'descricao'],
                      'str_args': '(nome, coordenadas, descricao) VALUES (?, ?, ?)'},
            'caverna': {'name': 'Cavernas',
                        'args': ['nome', 'coordenadas', 'tamanho', 'explorada'],
                        'str_args': '(nome, coordenadas, tamanho, explorada) VALUES (?, ?, ?, ?)'},
            'paisagem': {'name': 'Paisagens',
                         'args': ['nome', 'coordenadas', 'beleza', 'descricao'],
                         'str_args': '(nome, coordenadas, beleza, descricao) VALUES (?, ?, ?, ?)'},
            'outro': {'name': 'Outros',
                      'args': ['nome', 'coordenadas', 'descricao'],
                      'str_args': '(nome, coordenadas, descricao) VALUES (?, ?, ?)'}
        }
        self._create_tables()

    def _check_table(self, table_name):
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,))
        return self.cursor.fetchone()

    def _create_tables(self):
        if not self._check_table('Estruturas'):
            self.cursor.execute('''CREATE TABLE Estruturas (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome VARCHAR(127) NOT NULL,
                                coordenadas VARCHAR(31) NOT NULL,
                                explorada VARCHAR(15) NOT NULL,
                                );''')

        if not self._check_table('Biomas'):
            self.cursor.execute('''CREATE TABLE Biomas (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome VARCHAR(127) NOT NULL,
                                coordenadas VARCHAR(31) NOT NULL,
                                descricao VARCHAR(255) NOT NULL,
                                );''')

        if not self._check_table('Cavernas'):
            self.cursor.execute('''CREATE TABLE Cavernas (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome VARCHAR(127) NOT NULL,
                                coordenadas VARCHAR(31) NOT NULL,
                                tamanho VARCHAR(63) NOT NULL,
                                explorada VARCHAR(15) NOT NULL,
                                );''')

        if not self._check_table('Paisagens'):
            self.cursor.execute('''CREATE TABLE Paisagens
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome VARCHAR(127) NOT NULL,
                                coordenadas VARCHAR(31) NOT NULL,
                                beleza INTEGER NOT NULL,
                                descricao VARCHAR(255) NOT NULL);''')

        if not self._check_table('Outros'):
            self.cursor.execute('''CREATE TABLE Outros (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome VARCHAR(127) NOT NULL,
                                coordenadas VARCHAR(31) NOT NULL,
                                descricao VARCHAR(255) NOT NULL);''')

        self.conn.commit()

    def add(self, category, category_args):
        """
        Adds a new row to the specified category in the database.

        Args:
            category (str): The name of the category to add the row to.
            category_args (dict): A dictionary containing the values to insert into the row.

        Returns:
            bool: True if the row was successfully added, False otherwise.
        """
        category_ = self.categories.get(category, None)
        if not category_:
            return False
        category_name = category_.get('name', None)
        if not category_name:
            return False
        args_ = category_.get('args', None)
        if not args_:
            return False
        args_ = tuple(category_args.values())
        str_args = category_.get('str_args', None)
        if not str_args:
            return False

        self.cursor.execute(f"INSERT INTO {category_name} {str_args}", args_)

        self.conn.commit()
        return True

    def edit(self, category, id_, key, value):
        """
            Edits a specific value in the database for a given category and ID.

            Args:
                category (str): The category of the value to edit.
                id_ (int): The ID of the value to edit.
                key (str): The key of the value to edit.
                value (str): The new value to set.

            Returns:
                bool: True if the value was successfully edited, False otherwise.
        """
        category_ = self.categories.get(category, None)
        if not category_:
            return False
        category_name = category_.get('name', None)
        if not category_name:
            return False
        key_ = category_.get('args', None)
        if not key_:
            return False

        self.cursor.execute(f"UPDATE {category_name} SET {key}=? WHERE id=?", (value, id_))
        self.conn.commit()
        return True

    def delete(self, category, id_):
        """
            Deletes a row from a given category table based on the id.

            Args:
            category (str): The category of the table to delete from.
            id_ (int): The id of the row to delete.

            Returns:
            bool: True if the row was successfully deleted, False otherwise.
        """
        category_ = self.categories.get(category, None)
        if not category_:
            return False
        category_name = category_.get('name', None)
        if not category_name:
            return False

        self.cursor.execute(f"DELETE FROM {category_name} WHERE id=?", (id_,))
        self.conn.commit()
        return True
