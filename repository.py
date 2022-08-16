import sqlite3


class SQLiteRepository:
    def __connect(self, db_name: str):
        self.sqlite_connection = sqlite3.connect(db_name + '.db')
        self.cursor = self.sqlite_connection.cursor()

    def __close(self):
        self.cursor.close()
        self.sqlite_connection.close()

    def __execute_command(self, command):
        try:
            self.__connect(self.db_name)
            return command()

        except sqlite3.Error as error:
            print(f'error while {command.__name__}: {error}')

        finally:
            self.__close()

    def __init__(self, db_name='table1', key_name='key', value_name='value'):
        self.db_name = db_name
        self.key_name = key_name
        self.value_name = value_name
        self.sqlite_connection = None
        self.cursor = None

        def init_command():
            create_table_query = (f'CREATE TABLE {self.db_name} (\n'
                                  f'{self.key_name} TEXT NOT NULL,\n'
                                  f'{self.value_name} TEXT NOT NULL);')

            self.cursor.execute(create_table_query)
            self.sqlite_connection.commit()

        self.__execute_command(init_command)

    def create(self, key, value):
        def create_command():
            insert_query = (f'INSERT INTO {self.db_name}\n'
                            f'({self.key_name}, {self.value_name}) '
                            f'VALUES (\'{key}\', \'{value}\');')
            self.cursor.execute(insert_query)
            self.sqlite_connection.commit()

        self.__execute_command(create_command)

    def read(self, key):
        def read_command():
            read_query = f'SELECT * FROM {self.db_name} WHERE {self.key_name} = \'{key}\''
            self.cursor.execute(read_query)
            return self.cursor.fetchall()[0][1]

        return self.__execute_command(read_command)

    def read_all(self):
        def read_all_command():
            select_query = f'SELECT * FROM {self.db_name}'
            self.cursor.execute(select_query)
            return self.cursor.fetchall()

        return self.__execute_command(read_all_command)

    def delete(self, key):
        def delete_command():
            delete_query = f'DELETE FROM {self.db_name} WHERE {self.key_name} = \'{key}\''
            self.cursor.execute(delete_query)
            self.sqlite_connection.commit()

        self.__execute_command(delete_command)

    def delete_table(self):
        def delete_table_command():
            delete_table_query = f'''DROP table if exists {self.db_name}'''
            self.cursor.execute(delete_table_query)
            self.sqlite_connection.commit()

        self.__execute_command(delete_table_command)

    def update(self, key, value):
        def update_command():
            update_query = f'UPDATE table1 SET {self.value_name} = \'{value}\' where {self.key_name} = \'{key}\''
            self.cursor.execute(update_query)
            self.sqlite_connection.commit()

        self.__execute_command(update_command)


class FileRepository:
    storage = {}

    def create(self, key, value):
        self.storage[key] = value

    def read(self, key):
        return self.storage[key]

    def read_all(self):
        temp = []
        for key in self.storage:
            temp.append((key, self.storage[key]))
        return temp

    def delete(self, key):
        self.storage.pop(key)

    def update(self, key, value):
        if key not in self.storage:
            raise Exception(f'{key} is not created')
        self.storage[key] = value


def test(hashes):
    temp = []
    hashes.create('lavr', '228')
    temp.append(hashes.read_all())
    hashes.create('misha', '322')
    temp.append(hashes.read_all())
    hashes.update('lavr', '111')
    temp.append(hashes.read_all())
    temp.append(hashes.read('misha'))
    hashes.delete('misha')
    temp.append(hashes.read_all())
    return temp


sqlite_hashes = SQLiteRepository()
file_hashes = FileRepository()

a = test(sqlite_hashes)
print(*a)
sqlite_hashes.delete_table()
print()
b = test(file_hashes)
print(*b)
print(a == b)
