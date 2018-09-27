from header import Header


class Request(Header):

	def __init__(self, code, filename, mode):

		Header.__init__(self, code)

		self.file = bytearray(filename.encode('utf-8'))

		self.packet += self.file

		self.packet.append(0)

		self.mode = bytearray(mode.encode('utf-8'))

		self.packet += self.mode

		self.packet.append(0)
