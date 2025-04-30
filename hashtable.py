
class HashTable:
    def __init__(self, sizeOf):
        self.sizeOf = sizeOf
        self.table = [None] * sizeOf


    def _hash(self, key):
        return hash(key) % self.sizeOf
    

    def get(self, key):
        index = self._hash(key)
        if self.table[index] is not None:
            for pair in self.table[index]:
                if pair[0] == key:
                    return pair[1]
        return None
    

    def set(self, key, obj):
        index = self._hash(key)
        if self.table[index] is None:
            self.table[index] = []

        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = obj
                return
        
        self.table[index].append([key, obj])

    def delete(self, key):
        index = self._hash(key)
        
        if self.table[index] is not None:
            for i, pair in enumerate(self.table[index]):
                if pair[0] == key:
                    del self.table[index][i]
                    return True
        return False


## Test case

if __name__ == '__main__':
    testHash = HashTable(137)
    testHash.set(5, "It's my life")
    testHash.set(32, "It's now or never")
    testHash.set(800, "Something Something")
    testHash.set(41, "I don't want to live forever")

    print( testHash.get(5) )
    print( testHash.get(1) )
    print( testHash.get(41) )