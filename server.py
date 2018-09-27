from net import Net


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

			data = connection_socket.recv(516)

			connection_socket.close()
			break


if __name__ == '__main__':
	server = Server()

