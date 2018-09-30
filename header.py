# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol

# The parent to all packets, contains the op-code header
class Header:

	def __init__(self, set_code):
		# create a packet via a bytearray
		self.packet = bytearray()
		# putting in the 2 bytes for the op code
		self.packet.append(0)
		self.packet.append(set_code)

