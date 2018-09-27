from header import Header


class Error(Header):

	def __init__(self, err_code):
		# Since this is just for errors, only one op code is available
		Header.__init__(self, 5)

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
		if err_code == 1:
			self.packet.append("File not found.")
			self.packet.append(0)
		elif err_code == 5:
			self.packet.append("Unknown transfer ID.")
			self.packet.append(0)
		elif err_code == 6:
			self.packet.append("File already exists.")
			self.packet.append(0)
