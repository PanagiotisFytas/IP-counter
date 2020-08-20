import shelve
import os
import threading

class DataSink:
    def __init__(self, max_cache_size=10000):
        """
        DataSink is responsible for keeping track of the IPs in persistent storage
        :param max_cache_size: Integer, the maximum length allowed for the cache. If 0, no cache is used
        :return: an instance of the DataSink
        """
        self.unique_address_counter = 0

        self.lock = threading.Lock()

        try:
            # remove the sink to achieve consistency only since
            # the start of the service
            os.remove('ips.sink')
        except FileNotFoundError:
            pass

        if max_cache_size == 0:
            self.use_cache = False
            # Use a shelve object as a persistence storage
            # a shelve object is a python dictionary saved in disk
            self.sink = shelve.open("ips.sink")
            self.cache = None
            self.max_cache_size = max_cache_size
        else:
            self.use_cache = True
            # If using a cache put writeback=True so the dictionary
            # is only written in disk upon request
            self.sink = shelve.open("ips.sink", writeback=True)
            self.cache = set()
            self.max_cache_size = max_cache_size

    def write(self, ip):
        """
        If a cache is used, write an IP in the cache.
        If the cache is full write the cache in disk.
        If not cahce is used, write the IP in disk.
        :param ip: String, the IP to be written
        :return None
        """
        if self.use_cache:
            with self.lock:
                self.cache.add(ip)
                if len(self.cache) == self.max_cache_size:
                    # chache is full and will be written in data sink
                    self._write_cache_in_sink()
        else:
            self._write_in_sink(ip)

    def get_unique_addresses_counter(self):
        """
        If using a cache, the cache will be written in disk and the total number
        of unique ips will be calculated
        :return the number of unique IP adresses
        """
        if self.use_cache:
            # empty the cache and update the unique address counter
            with self.lock:
                self._write_cache_in_sink()
        return self.unique_address_counter

    def _write_cache_in_sink(self):
        """
        Writes the Cache in Sink.
        Updates the total unique IPs in the Sink.
        """
        unique_addresses_in_cache = 0
        for ip in self.cache:
            self._write_in_sink(ip)
        self.sink.sync()

    def _write_in_sink(self, ip):
        """
        If the ip does not exist in the Sink, write it and update the counter.
        :param ip: String : the IP adress
        """
        if ip not in self.sink:
            self.unique_address_counter += 1
            self.sink[ip] = None  # empty values



