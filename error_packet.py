# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol
from header import Header


class Error(Header):

	def __init__(self, err_code, in_message=''):
		# Since this is just for errors, only one op code is available
		Header.__init__(self, 5)
		self.packet.append(0)
		self.packet.append(err_code)
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
			self.packet.append(in_message.encode('utf-8'))
		elif err_code == 1:
			message = 'File not found.'
			self.packet += message.encode('utf-8')
			self.packet.append(0)
		elif err_code == 3:
			message = 'Disk full or allocation exceeded.'
			self.packet += message.encode('utf-8')
			self.packet.append(0)
		elif err_code == 5:
			message = "Unknown transfer ID."
			self.packet += message.encode('utf-8')
			self.packet.append(0)
		elif err_code == 6:
			message = "File already exists."
			self.packet += message.encode('utf-8')
			self.packet.append(0)
