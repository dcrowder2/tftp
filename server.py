# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol
from net import Net
from packet import Packet
from os import path

class Server(Net):

	def __init__(self):
		# Run super initializer
		Net.__init__(self)

		# add flags for server into argparse
		self.parser.add_argument('-v', action='store_true', help='Flag for verbose mode')

		# parse the arguments
		args = self.parser.parse_args()

		# bind the socket to the port
		self.sock.bind(('', args.p))
		self.sock.listen(1)
		if args.v:
			print("Server IP: " + str(self.sock.getsockname()) + "\nPort number: " + str(args.p) + "\nWaiting for connection")
		else:
			print("Ready to receive")
		while True:
			connection_socket, address = self.sock.accept()

			if args.v:
				print("Connection made with " + str(address))

			packet = connection_socket.recv(516)

			read_packet = Packet.read_packet(packet)

			# Kill packet received
			if read_packet[0] == 'end':
				connection_socket.close()
				self.sock.close()
				exit(0)

			if read_packet[0]:
				# Since a file added to the server will be preappended with 'new', this needs to be checked as well
				if path.exists(read_packet[1]) or path.exists('new'+read_packet[1]):
					return_packet = Packet.error(6)
					connection_socket.send(return_packet)
				else:
					connection_socket.send(Packet.ack(0))
					Net.receive_data(self, read_packet[1], connection_socket)
			else:
				if path.exists('new' + read_packet[1]):
					pathname = 'new' + read_packet[1]
				else:
					pathname = read_packet[1]
				# Sending a file not found error, this is redundant check if there is a 'new' + filename but if there
				#  isn't one this one checks for the original name
				if not path.exists(pathname):
					send_packet = Packet.error(1)
					connection_socket.send(send_packet)
				else:
					connection_socket.send(Packet.ack(0))
					Net.send_data(self, pathname, connection_socket)

			connection_socket.close()


if __name__ == '__main__':
	server = Server()

