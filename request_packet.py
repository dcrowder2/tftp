# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol
from header import Header


class Request(Header):

	def __init__(self, code, filename, mode):

		Header.__init__(self, code)

		encoded = filename.encode('utf-8')
		self.packet += bytearray(encoded)
		self.packet.append(0)

		encoded = mode.encode('utf-8')
		self.packet += bytearray(encoded)
		self.packet.append(0)
