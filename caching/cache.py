from memory import Memory
import utilities
import random
from collections import deque

# This class simply adds a variable that will keep track of cache
# hits. This should be incremented in a subclass whenever the cache is hit.
# 
class AbstractCache(Memory):
    def name(self):
        return "Cache"

    # Takes two parameters. 
    # Data is the data that forms the "memory". 
    # Size is a non-negative integer that indicates the size of the cache.
    # 
    def __init__(self, data, size=5):
        super().__init__(data)
        self.cache_hit_count = 0

    # Returns information on the number of cache hit counts
    def get_cache_hit_count(self):
        # TODO: Edit this code to correctly return the count of cache hits.
        return self.cache_hit_count
    
class CyclicCache(AbstractCache):
    def name(self):
        return "Cyclic"

    def __init__(self, data, size=5):
        super().__init__(data, size)
        self.cache = {}
        self.cache_keys = [None] * size
        self.cache_pointer = 0

    def lookup(self, address):
        # case in cache
        if address in self.cache:
            self.cache_hit_count += 1
            return self.cache[address]

        # case not in cache
        value = super().lookup(address)
        # remove old key from cache if necessary
        old_key = self.cache_keys[self.cache_pointer]
        if old_key is not None:
            del self.cache[old_key]
        
        # update cache with new value
        self.cache[address] = value
        self.cache_keys[self.cache_pointer] = address
        
        # update pointer (in case size of cache changes)
        self.cache_pointer = (self.cache_pointer + 1) % len(self.cache_keys)

        return value
  
        
    

class LRUCache(AbstractCache):
    def name(self):
        return "LRU"

    def __init__(self, data, size=5):
        super().__init__(data, size)
        self.cache = {}
        self.lru_queue = deque(maxlen=size)

    def lookup(self, address):
        # case in cache
        if address in self.cache:
            self.cache_hit_count += 1
            value = self.cache[address]

            # update LRU queue
            self.lru_queue.remove(address)
            self.lru_queue.append(address)

            return value

        # case not in cache
        value = super().lookup(address)

        # case cache is full
        if len(self.cache) == self.lru_queue.maxlen:
            least_recently_used_key = self.lru_queue.popleft()
            del self.cache[least_recently_used_key]

        # case not full, add to cache and update LRU queue
        self.cache[address] = value
        self.lru_queue.append(address)

        return value
    

class RandomCache(AbstractCache):
    def name(self):
        return "Random"

    def __init__(self, data, size=5):
        super().__init__(data, size)
        self.cache = {}
        self.cache_keys = [None] * size
        self.cache_size = size

    def lookup(self, address):
        # case in cache
        if address in self.cache:
            self.cache_hit_count += 1
            return self.cache[address]

        # case not in cache
        value = super().lookup(address)

        # check if any space in cache is None
        if None in self.cache_keys:
            index = self.cache_keys.index(None)
            self.cache_keys[index] = address
            self.cache[address] = value
        # if not, then find a random place and put the nextValue in
        else:
            evicted_key = random.choice(self.cache_keys)
            del self.cache[evicted_key]

            index = self.cache_keys.index(evicted_key)
            self.cache_keys[index] = address
            self.cache[address] = value

        return value