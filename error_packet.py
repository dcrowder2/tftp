# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol
from header import Header
import bitstring


class Error(Header):

	def __init__(self, err_code, d_port, s_port, seq_num, in_message=''):
		# Since this is just for errors, only one op code is available
		Header.__init__(self, seq_num, s_port, d_port, fin=True)
		# Implementing the error message
		# 0 Not defined, see error message (if any).
		# 1 File not found.
		# 2 Access violation.
		# 3 Disk full or allocation exceeded.
		# 4 Illegal TFTP operation.
		# 5 Unknown transfer ID.
		# 6 File already exists.
		# 7 No such user.
		if err_code == 0:
			message = in_message
		elif err_code == 1:
			message = 'File not found.'
		elif err_code == 3:
			message = 'Disk full or allocation exceeded.'
		elif err_code == 5:
			message = "Unknown transfer ID."
		elif err_code == 6:
			message = "File already exists."
		else:
			message = "Unknown Error"
		self.error = bitstring.BitArray(message.encode('utf-8'))
		self.error_code = err_code

	def combine(self):
		complete = super(Error, self).combine()
		# to signify an error packet, I start the data with 7 0s and 9 1s which shouldn't match any other data
		complete.append(bitstring.BitArray(7))
		complete.append(bitstring.Bits('0b111111111'))
		complete.append(bin(self.error_code))
		complete.append(self.error)
		return complete

	def calc_checksum(self):
		super(Error, self).calc_checksum()
