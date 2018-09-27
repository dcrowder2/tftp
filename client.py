from net import Net


class Client(Net):

	def __init__(self):
		# run the super initializer
		Net.__init__(self)
		# add the specific arguments for a client server

		self.parser.add_argument('-f', metavar='filename', type=str, help='The filename of a file to write/read')
		self.parser.add_argument('-a', metavar='address', type=str, help='The ip address of the server')
		self.parser.add_argument('-w', action='store_true', help='Flag for writing a file')
		self.parser.add_argument('-r', action='store_true', help='Flag for reading a file')

		# parse the arguments
		args = self.parser.parse_args()

		# Connect to the server
		self.sock.connect((args.a, args.p))

		# Writing a file
		if args.w:
			self.file = open(args.f, "rb")
			for line in self.file:
				self.sock.send(line)


if __name__ == '__main__':
	client = Client()