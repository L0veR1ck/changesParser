class Container:
    def __init__(self):
        self.storage = {}

    def create(self, table_name, table_data=None):
        if data is None:
            table_data = {}
        if table_name in self.storage:
            print(f'Name \'{table_name}\' is already taken')
            return
        self.storage[table_name] = table_data

    def read(self, table_name=None):
        if table_name is None:
            return self.storage
        try:
            return self.storage[table_name]
        except:  # почему подчеркивает? исправить на finally помогает, но вроде логичнее except
            print(f'Table \'{table_name}\' does not exist')
            return

    def delete(self, table_name):
        self.storage.pop(table_name)

    def update(self, table_name, new_data):  # наверное надо как то умнее :)
        self.delete(table_name)
        self.create(table_name, new_data)


data = Container()
users = {'l0ver1ck': 228, 'snoward': 322}
kekers = ['keker1', 'keker2']
data.create('users', users)
data.create('kekers', kekers)
print(data.read())
data.create('users', ['lolik', 'nolik'])
data.read('abdul')
