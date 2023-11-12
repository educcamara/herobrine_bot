import sqlite3


class SQLManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.categories = {
            'estrutura': {'name': 'Estruturas', 'args': ['nome', 'coordenadas', 'explorada']},
            'bioma': {'name': 'Biomas', 'args': ['nome', 'coordenadas', 'descricao']},
            'caverna': {'name': 'Cavernas', 'args': ['nome', 'coordenadas', 'tamanho', 'explorada']},
            'paisagem': {'name': 'Paisagens', 'args': ['nome', 'coordenadas', 'beleza', 'descricao']},
            'outro': {'name': 'Outros', 'args': ['nome', 'coordenadas', 'descricao']}
        }
        self._create_tables()

    def _check_table(self, table_name):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
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

    def add(self, category, name, coordinates, category_args):
        if category == 'estrutura':
            self.cursor.execute("INSERT INTO Estruturas (nome, coordenadas, explorada) VALUES (?, ?, ?)",
                                (name,
                                 coordinates,
                                 category_args.get('explorada', 'NULL')))
        elif category == 'bioma':
            self.cursor.execute("INSERT INTO Biomas (nome, coordenadas, descricao) VALUES (?, ?, ?)",
                                (name,
                                 coordinates,
                                 category_args.get('descricao', 'NULL')))
        elif category == 'caverna':
            self.cursor.execute("INSERT INTO Cavernas (nome, coordenadas, tamanho, explorada) VALUES (?, ?, ?, ?)",
                                (name,
                                 coordinates,
                                 category_args.get('tamanho', 'NULL'),
                                 category_args.get('explorada', 'NULL')))
        elif category == 'paisagem':
            self.cursor.execute("INSERT INTO Paisagens (nome, coordenadas, beleza, descricao) VALUES (?, ?, ?, ?)",
                                (name,
                                 coordinates,
                                 category_args.get('beleza', -1),
                                 category_args.get('descricao', 'NULL')))
        elif category == 'outro':
            self.cursor.execute("INSERT INTO Outros (nome, coordenadas, descricao) VALUES (?, ?, ?)",
                                (name,
                                 coordinates,
                                 category_args.get('descricao', 'NULL')))
        else:
            return False

        self.conn.commit()
        return True

    def edit(self, category, id_, key, value):
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
        category_ = self.categories.get(category, None)
        if not category_:
            return False
        category_name = category_.get('name', None)
        if not category_name:
            return False

        self.cursor.execute(f"DELETE FROM {category_name} WHERE id=?", (id_,))
        self.conn.commit()
        return True
