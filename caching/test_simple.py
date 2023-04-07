from memory import Memory
from cache import CyclicCache, LRUCache, RandomCache
import utilities
import unittest

# A collection of basic unit tests for caching. These tests will check
# some basic aspects of the implementation, but should not be considered comprehensive in any way. 

# Stop unittest printing traces out. Uncomment this line if you want
# to see trace information
__unittest = True

class BasicTestCase(unittest.TestCase):

    def setUp(self):
        data = utilities.sample_data(size=100)
        # This test suite assumes that the cache is of size
        # 5. Changing this may result in some tests failing.
        self.memory = Memory(data)
        self.cyclic = CyclicCache(data)
        self.lru = LRUCache(data)
        self.random = RandomCache(data)

# Unit tests
class TestCaseLookup(BasicTestCase):

    # Simple lookup comparisons. The results of looking up a location
    # twice should be the same
    def lookup_check(self, impl, location):
        # Lookup location. Should be non null.
        datum_1 = impl.lookup(location)
        self.assertTrue(datum_1)

        # Lookup location again. Should still be non null.
        datum_2 = impl.lookup(location)
        self.assertTrue(datum_2)
        
        # The two results should be equal
        self.assertEqual(datum_1, datum_2, "Lookup results don't match")

    # Memory
    def test_memory(self):
        self.lookup_check(self.memory, 0)
        self.lookup_check(self.memory, 10)

    # Cyclic
    def test_cyclic(self):
        self.lookup_check(self.cyclic, 0)
        self.lookup_check(self.cyclic, 10)

    # LRU
    def test_lru(self):
        self.lookup_check(self.lru, 0)
        self.lookup_check(self.lru, 10)

    # Random
    def test_random(self):
        self.lookup_check(self.random, 0)
        self.lookup_check(self.random, 10)


class TestCaseMemoryHit(BasicTestCase):

    # Lookup the same location twice and check the hit count
    def caching_check(self, impl, diff):
        # Warm up and fill the cache.
        for loc in range(10,20):
            impl.lookup(loc)

        # Lookup location 1
        datum_1 = impl.lookup(1)
        hits_1 = impl.get_memory_hit_count()

        # Lookup location 1
        datum_2 = impl.lookup(1)
        hits_2 = impl.get_memory_hit_count()
        # If the cache is working, then the hit count should have
        # changed by the given amount
        self.assertEqual(hits_1+diff, hits_2, "Memory hit count incorrect")

    # Memory. Hit count should increase by 1
    def test_memory(self):
        self.caching_check(self.memory, 1)

    # Cyclic. Hit count should not increase as the cache should be used.
    def test_cyclic(self):
        self.caching_check(self.cyclic, 0)

    # LRU. Hit count should not increase as the cache should be used
    def test_lru(self):
        self.caching_check(self.lru, 0)

    # Random. Hit count should not increase as the cache should be used
    def test_random(self):
        self.caching_check(self.random, 0)

class TestCaseCacheHit(BasicTestCase):

    # Lookup the same location twice and check the cache hit count
    def caching_check(self, impl, diff):
        # Warm up and fill the cache.
        for loc in range(10,20):
            impl.lookup(loc)

        # Lookup location 1
        datum_1 = impl.lookup(1)
        hits_1 = impl.get_cache_hit_count()

        # Lookup location 1
        datum_2 = impl.lookup(1)
        hits_2 = impl.get_cache_hit_count()
        # If the cache is working, then the hit count should have
        # changed by the given amount
        self.assertEqual(hits_1+diff, hits_2, "Cache hit count incorrect")

    # Memory. Cache hit count should not increase as the cache should be used.
    def test_memory(self):
        self.caching_check(self.memory, 0)

    # Cyclic. Cache hit count should increase as the cache should be used.
    def test_cyclic(self):
        self.caching_check(self.cyclic, 1)

    # LRU. Cache hit count should increase as the cache should be used
    def test_lru(self):
        self.caching_check(self.lru, 1)

    # Random. Cache hit count should increase as the cache should be used
    def test_random(self):
        self.caching_check(self.random, 1)

class TestCaseMultipleLookup(BasicTestCase):

    # Here we look up five items, then request the first one again.
    # Then check the hit counts.
    def caching_check(self, impl, diff):
        # Warm up and fill the cache.
        for loc in range(10,20):
            impl.lookup(loc)

        # Look up 5 items
        datum_1 = impl.lookup(1)
        datum_2 = impl.lookup(2)
        datum_3 = impl.lookup(3)
        datum_4 = impl.lookup(4)
        datum_5 = impl.lookup(5)
        hits_1 = impl.get_memory_hit_count()
        datum_6 = impl.lookup(1)
        hits_2 = impl.get_memory_hit_count()
        # Data should be the same
        self.assertEqual(datum_1, datum_6, "Lookup values don't match")
        # If the cache is working, then the hit count should have
        # changed by the given amount
        self.assertEqual(hits_1+diff, hits_2, "Memory hit count incorrect")

    # Memory. Hit count should increase by 1
    def test_memory(self):
        self.caching_check(self.memory, 1)

    # Cyclic. Hit count should not increase as the cache should be used.
    def test_cyclic(self):
        self.caching_check(self.cyclic, 0)

    # LRU. Hit count should not increase as the cache should be used.
    def test_lru(self):
        self.caching_check(self.lru, 0)

    # Note that we can't perform this test for the random strategy as
    # 1 *may* be evicted during the lookup of the five items.

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestCaseLookup('test_memory'))
    suite.addTest(TestCaseLookup('test_cyclic'))
    suite.addTest(TestCaseLookup('test_lru'))
    suite.addTest(TestCaseLookup('test_random'))
    suite.addTest(TestCaseMemoryHit('test_memory'))
    suite.addTest(TestCaseMemoryHit('test_cyclic'))
    suite.addTest(TestCaseMemoryHit('test_lru'))
    suite.addTest(TestCaseMemoryHit('test_random'))
    suite.addTest(TestCaseCacheHit('test_memory'))
    suite.addTest(TestCaseCacheHit('test_cyclic'))
    suite.addTest(TestCaseCacheHit('test_lru'))
    suite.addTest(TestCaseCacheHit('test_random'))
    suite.addTest(TestCaseMultipleLookup('test_memory'))
    suite.addTest(TestCaseMultipleLookup('test_cyclic'))
    suite.addTest(TestCaseMultipleLookup('test_lru'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
