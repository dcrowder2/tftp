from header import Header


class Request(Header):

	def __init__(self, code, filename, mode):

		Header.__init__(self, code)

		encoded = filename.encode('utf-8')
		self.packet += encoded
		self.packet.append(0)

		encoded = mode.encode('utf-8')
		self.packet += encoded
		self.packet.append(0)
