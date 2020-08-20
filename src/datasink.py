import shelve
import os

class DataSink:
    def __init__(self, max_cache_size=10000):

        self.unique_address_counter = 0

        try:
            # remove the sink to achieve consistency only since
            # the start of the service
            os.remove('ips.sink')
        except FileNotFoundError:
            pass

        if max_cache_size == 0:
            self.use_cache = False
            self.sink = shelve.open("ips.sink")
            self.cache = None
            self.max_cache_size = max_cache_size
        else:
            self.use_cache = True
            self.sink = shelve.open("ips.sink", writeback=True)
            self.cache = set()
            self.max_cache_size = max_cache_size

