import pickle


class Header:

	def __init__(self, set_code):
		self.head = bytearray()
		self.head.append(0)
		self.head.append(set_code)

