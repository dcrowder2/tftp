# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol
from net import Net
from packet import Packet
from os import path


class Client(Net):

	def __init__(self):
		# run the super initializer
		Net.__init__(self)
		# add the specific arguments for a client server

		self.parser.add_argument('-f', metavar='filename', type=str, help='The filename of a file to write/read')
		self.parser.add_argument('-a', metavar='address', type=str, help='The ip address of the server')
		self.parser.add_argument('-w', action='store_true', help='Flag for writing a file')
		self.parser.add_argument('-r', action='store_true', help='Flag for reading a file')
		self.parser.add_argument('-k', action='store_true', help='Flag for killing the server')

		# parse the arguments
		args = self.parser.parse_args()

		# if you want to kill, open connection, and send kill
		if args.k:
			self.sock.connect((args.a, args.p))
			self.sock.send(Packet.kill())
			exit(0)

		if not path.exists(args.f):
			print("File not found, please enter a valid filename")
			exit(0)

		# Connect to the server
		self.sock.connect((args.a, args.p))

		# Writing a file
		if args.w:
			self.sock.send(Packet.request(args.f, 'netascii', True))
			receive = self.sock.recv(516)
			ack = Packet.read_packet(receive)
			# Check for the correct ack for the request, if not terminate the connection via an empty data packet
			if ack[0] == 0:
				Net.send_data(self, args.f, self.sock)
			else:
				self.sock.close(Packet.data(0, b''))
		else:
			self.sock.send(Packet.request(args.f, 'netascii', False))
			ack = Packet.read_packet(self.sock.recv(516))
			# check for the correct ack for the request, if not terminate the connection via an empty data packet
			if ack[0] == 0:
				Net.receive_data(self, args.f, self.sock)
			else:
				self.sock.send(Packet.data(0, b''))
		self.sock.close()


if __name__ == '__main__':
	client = Client()
