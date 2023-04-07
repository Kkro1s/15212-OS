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

    # TODO: Edit the code below to provide an implementation of a cache that
    # uses a cyclic caching strategy with the given cache size. You
    # can use additional methods and variables as you see fit as long
    # as you provide a suitable overridding of the lookup method.
    # Make sure that you increment cache_hit_count when appropriate!
    
    def __init__(self, data, size=5):
        super().__init__(data,size)
        #cache as a array
        self.cache = []*size
        self.cache_pointer = 0

    def lookup(self, nextValue):
        #case in cache
        if nextValue in self.cache:
            self.cache_hit_count += 1
            return True

        #case not
        self.cache[self.cache_pointer] = nextValue
        #update pointer(incase size of cache changes)
        self.cache_pointer = (self.cache_pointer + 1) % len(self.cache)
        return False

        
    

class LRUCache(AbstractCache):
    def name(self):
        return "LRU"

    # TODO: Edit the code below to provide an implementation of a cache that
    # uses a least recently used caching strategy with the given cache size.
    # You can use additional methods and variables as you see fit as
    # long as you provide a suitable overridding of the lookup method.
    # Make sure that you increment cache_hit_count when appropriate!
    
    def __init__(self, data, size=5):
        super().__init__(data)
        #create deque as a cache
        self.cache = deque(maxlen = size)
    def lookup(self, nextValue):
        if next in self.cache:
            self.cache_hit_count += 1
        #put this value in the first
            if self.cache.index(nextValue) == 0:
                return True
            else:
                self.cache.remove(nextValue)
                self.cache.appendleft(nextValue)
                return True
        #case cache is full       
        if len(self.cache) == self.cache.maxlen:
            self.cache.pop()
        #case not full and append it 
        self.cache.appendleft(nextValue)
        return False
class RandomCache(AbstractCache):
    def name(self):
        return "Random"

    # TODO: Edit the code below to provide an implementation of a cache that
    # uses a random eviction strategy with the given cache size.
    # You can use additional methods and variables as you see fit as
    # long as you provide a suitable overridding of the lookup method.
    # Make sure that you increment cache_hit_count when appropriate!
    
    def __init__(self, data, size=5):
        super().__init__(data,size)
        self.cache = []*size
    
    def lookup(self,nextValue):
        if nextValue in self.cache:
            self.cache_hit_count += 1
            return True
        # check any space in cache is None
        if None is self.cache:
            self.cache[self.cache.index(None)] = nextValue
        # if is not then find a random place and put the nextValue in
        else:
            self.cache[random.randint(0,len(self.cache)-1)] = nextValue