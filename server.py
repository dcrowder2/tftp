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

			if read_packet[0]:
				if path.exists(read_packet[1]):
					return_packet = Packet.error(6)
					connection_socket.send(return_packet)
					connection_socket.close()
				else:
					connection_socket.send(Packet.ack(0))
					Net.receive_data(self, read_packet[1], connection_socket)
			else:
				connection_socket.send(Packet.ack(0))
				Net.send_data(self, read_packet[1], connection_socket)

			connection_socket.close()


if __name__ == '__main__':
	server = Server()

