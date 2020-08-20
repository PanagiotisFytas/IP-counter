import unittest
from src.datasink import DataSink

class Testing(unittest.TestCase):
    def test__write_in_sink(self):
        ds = DataSink()
        ds._write_in_sink('0.0.0.0')
        assert '0.0.0.0' in ds.sink
        assert ds.unique_address_counter == 1

    def test__write_cache_in_sink(self):
        ds = DataSink(max_cache_size=10)
        ds.cache = set(['0.0.0.0', '0.0.0.1', '0.0.0.2'])
        ds._write_cache_in_sink()
        assert ds.unique_address_counter == 3 # assert that everything is written once
        ds.cache = set(['0.0.0.0', '0.0.0.1', '0.0.0.2'])
        ds._write_cache_in_sink()
        assert ds.unique_address_counter == 3 # assert that duplicates are not written

    def test_write(self):
        ds = DataSink(max_cache_size=2)
        ds.write('0.0.0.0')
        assert ds.unique_address_counter == 0 # assert that it is not written on cache yet
        assert '0.0.0.0' not in ds.sink
        ds.write('0.0.0.1')
        assert ds.unique_address_counter == 2 # assert everything is written on cache
        assert '0.0.0.0' in ds.sink
        assert '0.0.0.1' in ds.sink
        
        # test no cache write
        ds = DataSink(max_cache_size=0)
        ds.write('0.0.0.0')
        assert ds.unique_address_counter == 1 # assert everything is written on cache
        assert '0.0.0.0' in ds.sink
        
    def test_get_unique_addresses_counter(self):
        # test when using a cache
        ds = DataSink(max_cache_size=10)
        ds.write('0.0.0.0')
        ds.write('0.0.0.1')
        ds.write('0.0.0.1')
        assert ds.get_unique_addresses_counter() == 2
        # test when not using a cache
        ds = DataSink(max_cache_size=0)
        ds.write('0.0.0.0')
        ds.write('0.0.0.1')
        ds.write('0.0.0.1')
        assert ds.get_unique_addresses_counter() == 2
        


if __name__ == '__main__':
    unittest.main()