from header import Header


class Request(Header):

	def __init__(self, code, filename, mode):

		Header.__init__(self, code)

		self.packet.append(filename)
		self.packet.append(0)
		self.packet.append(mode)
		self.packet.append(0)
