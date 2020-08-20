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

    def write(self, ip):
        self.cache.add(ip)
        if self.use_cache and len(self.cache) == self.max_cache_size:
            # chache is full and will be written in data sink
            self._write_cache_in_sink()

    def get_unique_addresses_counter(self):
        if self.use_cache:
            # empty the cache and update the unique address counter
            self._write_cache_in_sink()
        return self.unique_address_counter

    def _write_cache_in_sink(self):
        unique_addresses_in_cache = 0
        for ip in self.cache:
            if ip not in self.sink:
                unique_addresses_in_cache += 1
                self.sink[ip] = None  # empty values
        self.sink.sync()
        # update the total unique IP address counter
        self.unique_address_counter += unique_addresses_in_cache


