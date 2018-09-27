

class Header:

	def __init__(self, set_code):
		self.packet = bytearray()
		self.packet.append(set_code)

