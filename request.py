from header import Header


class Request(Header):

	def __init__(self, code, filename, mode):

		Header.__init__(self, code)

		self.file = bytearray(filename.encode('utf-8'))

		self.head += self.file

		self.head.append(0)

		self.mode = bytearray(mode.encode('utf-8'))

		self.head += self.mode

		self.head.append(0)
