class Repository:
    def __init__(self, data=None):
        if type(data) == dict:
            self.storage = data
        else:
            self.storage = {}

    def create(self, key, value):
        self.storage[key] = value

    def read(self, key):
        return self.storage[key]

    def read_all(self):
        return self.storage

    def delete(self, key):
        return self.storage.pop(key)

    def update(self, key, value):
        self.storage[key] = value


lavrHash = {'id': 123, 'value': 'DKFDHDKJFHD'}
hashes = Repository(lavrHash)
print(hashes.read_all())
hashes.update('value', 'KEK')
print(hashes.read_all())
