from header import Header


class Request(Header):

	def __init__(self, code):

		Header.__init__(self, code)