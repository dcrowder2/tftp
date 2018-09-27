from header import Header


# This class encompasses the duties for a data packet and a ack packet
class Datack(Header):

	def __init__(self, in_code):

		Header.__init__(self, in_code)

		# initialized to 0 because it should be the beginning of the block, with the first ack
		self.packet.append(0)
		# for a data packet, the data will be added by the client/server, and is dependent on the file they have open,
		# so no data will be added at this point
