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
			# Since the packet header will always be 20 bytes, the mtu is 1500 so 1480 bytes per read
			chunk = self.file.read(1452)
			chunk_list.append(chunk)
		return chunk_list
