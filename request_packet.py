# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol
from header import Header
import bitstring


class Request(Header):

	def __init__(self, code, filename, seq_num, s_port, d_port):

		if code == 1:
			Header.__init__(self, seq_num, s_port, d_port, 0, syn=True)
		else:
			Header.__init__(self, seq_num, s_port, d_port, 0, write=True, syn=True)

		self.data = bitstring.Bits(filename.encode('utf-8'))

	def combine(self):
		complete = super(Request, self).combine()
		complete.append(self.data)
		return complete

	def calc_checksum(self):
		super(Request, self).calc_checksum()
