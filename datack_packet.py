# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol
from header import Header
from error_packet import Error
import bitstring


# This class encompasses the duties for a data packet and a ack packet
class Datack(Header):

	def __init__(self, in_code, sequence_number, ack_number, d_port, s_port, data=b''):

		if in_code == 4:  # ack packet
			Header.__init__(self, sequence_number, s_port, d_port, ack_number, ack=True)

		if in_code == 3:  # data packet
			Header.__init__(self, sequence_number, s_port, d_port, ack_number)
			self.data = bitstring.BitArray(data)

	def combine(self):
		complete = super(Datack, self).combine()
		complete.append(self.data)
		return complete

	def calc_checksum(self):
		super(Datack, self).calc_checksum()
