class Repository:
    def __init__(self, data=None):
        if type(data) == dict:
            self.storage = data
        elif type(data) == None:
            self.storage = {}
        else:
            raise Exception('Data is not a dictionary')

    def create(self, key, value):
        self.storage[key] = value

    def read(self, key):
        return self.storage[key]

    def read_all(self):
        return self.storage

    def delete(self, key):
        return self.storage.pop(key)

    def update(self, key, value):
        if key not in self.storage:
            raise Exception(f'{key} is not created')
        self.storage[key] = value


lavrHash = {'id': 123, 'value': 'DKFDHDKJFHD'}
hashes = Repository(lavrHash)
print(hashes.read_all())
hashes.update('value', 'KEK')
print(hashes.read_all())
hashes.update('lol', 123)