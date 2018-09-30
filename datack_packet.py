# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol
from header import Header
from error_packet import Error


# This class encompasses the duties for a data packet and a ack packet
class Datack(Header):

	def __init__(self, in_code, block_number):

		Header.__init__(self, in_code)
		# If the block number goes over 1 byte, then it needs to be split so it can be put into the array
		if block_number < 256:
			self.packet.append(0)
			self.packet.append(block_number)
		# This is the max number of blocks that can be sent, as there is only 2 bytes for the block number
		elif block_number > 65534:
			self.packet = Error(3).packet
		else:
			first_part = block_number >> 8
			second_part = block_number & 255
			self.packet.append(first_part)
			self.packet.append(second_part)

		# for a data packet, the data will be added by the client/server, and is dependent on the file they have open,
		# so no data will be added at this point
