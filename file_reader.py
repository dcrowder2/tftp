# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol

class FileReader:

    def __init__(self, filename):
        self.file = open(filename, 'rb')

    def get_chunk(self, num_chunk):
        chunk_list = []
        for i in range(num_chunk):
            chunk = self.file.read(1400)  # TODO: check for actually chunk size
            chunk_list.append(chunk)
        return chunk_list
