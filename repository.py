import sqlite3


class Repository:
    def connect(self, db_name: str):
        self.sqlite_connection = sqlite3.connect(db_name + '.db')
        self.cursor = self.sqlite_connection.cursor()

    def close(self):
        self.cursor.close()
        self.sqlite_connection.close()

    def main(self, func):
        try:
            self.connect(self.db_name)
            func()

        except sqlite3.Error as error:
            print(error)
        finally:
            self.close()

    def __init__(self, db_name='table1', key_name='key', value_name='value'):
        self.db_name = db_name
        self.key_name = key_name
        self.value_name = value_name
        self.sqlite_connection = None
        self.cursor = None
        try:
            self.connect(self.db_name)
            create_table_query = (f'CREATE TABLE {self.db_name} (\n'
                                  f'{self.key_name} TEXT NOT NULL,\n'
                                  f'{self.value_name} TEXT NOT NULL);')

            self.cursor.execute(create_table_query)
            self.sqlite_connection.commit()

        except sqlite3.Error as error:
            print(error)
        finally:
            self.close()

    def create(self, key, value):
        def create2():
            insert_query = (f'INSERT INTO {self.db_name}\n'
                            f'({self.key_name}, {self.value_name}) '
                            f'VALUES (\'{key}\', \'{value}\');')

            self.cursor.execute(insert_query)
            self.sqlite_connection.commit()

        self.main(create2())

    def read(self, key):
        try:
            self.connect(self.db_name)
            read_query = f'SELECT * FROM {self.db_name} WHERE {self.key_name} = \'{key}\''
            self.cursor.execute(read_query)

            return self.cursor.fetchall()

        except sqlite3.Error as error:
            print(error)
        finally:
            self.close()

    def read_all(self):
        try:
            self.connect(self.db_name)
            select_query = f'SELECT * FROM {self.db_name}'
            self.cursor.execute(select_query)
            return self.cursor.fetchall()

        except sqlite3.Error as error:
            print(error)
        finally:
            self.close()

    def delete(self, key):
        try:
            self.connect(self.db_name)
            delete_query = f'DELETE FROM {self.db_name} WHERE {self.key_name} = \'{key}\''
            self.cursor.execute(delete_query)

            self.sqlite_connection.commit()

        except sqlite3.Error as error:
            print(error)
        finally:
            self.close()

    def delete_table(self):
        try:
            self.connect(self.db_name)
            delete_table_query = f'''DROP table if exists {self.db_name}'''

            self.cursor.execute(delete_table_query)
            self.sqlite_connection.commit()

        except sqlite3.Error as error:
            print(error)
        finally:
            self.close()

    def update(self, key, value):
        try:
            self.connect(self.db_name)
            update_query = f'UPDATE table1 SET {self.value_name} = \'{value}\' where {self.key_name} = \'{key}\''

            self.cursor.execute(update_query)
            self.sqlite_connection.commit()

        except sqlite3.Error as error:
            print(error)
        finally:
            self.close()


hashes = Repository()
hashes.create('lavr', '228')
print(hashes.read_all())
hashes.create('misha', '322')
print(hashes.read_all())
hashes.update('lavr', '111')
print(hashes.read_all())
print(hashes.read('misha'))
hashes.delete('misha')
print(hashes.read_all())
hashes.delete_table()
