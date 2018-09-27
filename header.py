# The parent to all packets, contains the op-code header
class Header:

	def __init__(self, set_code):
		# create a packet via a bytearray
		self.packet = []
		# I am not sure how big the set code is, but the size of the packet gets larger by 3 bytes
		self.packet.append(set_code)

