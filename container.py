class Repository:
    def __init__(self):
        self.storage = {}

    def create(self, data: dict):
        self.storage.update(data)

    def read(self, elem=None):
        if elem is None:
            return self.storage
        return self.storage[elem]

    def delete(self, elem):
        return self.storage.pop(elem)

    def update(self, new_data):
        self.storage.update(new_data)


hashes = Repository()
lavrHash = {'id': 123, 'value': 'DKFDHDKJFHD'}
hashes.create(lavrHash)
print(hashes.read())
lavrHash = {'id': 123, 'value': 'ZZZZZZZZZ'}
hashes.update(lavrHash)
print(hashes.read())
