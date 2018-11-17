from header import Header
from error_packet import Error
import bitstring


# This class encompasses the duties for a data packet and a ack packet
class Datack(Header):

	def __init__(self, in_code, block_number):

		Header.__init__(self, in_code)
		if in_code == 4:  # ack packet
			self.acknowledge_flag = bitstring.Bits(bin=1)
			self.acknowledge_number.append(bin(block_number))  # Block number will be data received for a ack packet

