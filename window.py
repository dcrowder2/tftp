# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol


# This is an object that will act as a window for Go back N
class Window:

	def __init__(self, size):
		self.size = size
		self.window = []

	def add_packets(self, packets):
		if len(self.window) == self.size - len(packets):
			for packet in packets:
				self.window.append(packet)
			return True
		else:
			return False

	def get_packet_space(self):
		return self.size - len(self.window)

	# this will remove all the packets up to the last_sequence_number which will be the ack number received back
	# after sending a packet, so it does go back N without any extra computation, since the packets that weren't
	# acked will be kept in the window
	def remove_packets(self, last_sequence_number):
		if len(self.window) > 0:
			i = 1

			for packet in self.window:
				if packet.sequence_number.uint != last_sequence_number:
					i += 1

			if i < len(self.window):
				for j in range(i):
					self.window.pop(0)
				return True
			else:
				return False
		else:
			return False
