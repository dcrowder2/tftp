# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol
from bitstring import BitArray


# This is an object that will act as a window for Go back N
class Window:

	def __init__(self, size):
		self.size = size
		print("Window created with size" + str(size))
		self.window = []

	def add_packets(self, packets):
		print("Adding " + str(len(packets)) + " to the window")
		for packet in packets:
			print("Adding packet " + str(packet.sequence_number) + " to the window")
			self.window.append(packet)
		print("Adding to window finished")

	def get_packet_space(self):
		return self.size - len(self.window)

	# this will remove all the packets up to the last_sequence_number which will be the ack number received back
	# after sending a packet, so it does go back N without any extra computation, since the packets that weren't
	# acked will be kept in the window
	def remove_packets(self, ack_number, error=False):
		if self.window:
			if error:
				i = 0
			else:
				i = 1
			last_sequence_number = ack_number - (len(self.window[-1].data) // 8)

			for packet in self.window:
				if packet.sequence_number.uint < last_sequence_number:
					i += 1

			if i <= len(self.window):
				print("Removing " + str(i) + " packets from the window")
				for j in range(i):
					print("Removing packet " + str(self.window.pop(0).sequence_number))
				return True
			else:
				return False
		else:
			return False

	def re_checksum(self):
		for packet in self.window:
			packet.checksum = BitArray('0b0000000000000000')
			packet.calc_checksum()

	def send(self, sock, d_address, d_port):
		for packet in self.window:
			print("Sending packet " + str(packet.sequence_number))
			sock.sendto(packet.binary_combine(), (d_address, d_port))
