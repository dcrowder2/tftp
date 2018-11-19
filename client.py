# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol
from net import Net
from packet import Packet
from os import path
import socket


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

		server_connection = (args.a, args.p)

		# if you want to kill, open connection, and send kill
		if args.k:
			self.sock.sendto(Packet.kill(), server_connection)
			exit(0)

		if not path.exists(args.f):
			print("File not found, please enter a valid filename")
			exit(0)

		# Creating connection to server
		# source port is 0 since the connection has been made yet
		print("Initiating connection")
		self.sock.sendto(Packet.request(args.f, args.w, args.p, 0, self.seq_number).binary_combine(), server_connection)
		self.sock.settimeout(2)
		try:
			syn_ack, address = self.sock.recvfrom(1472)
			read_syn = Packet.read_packet(syn_ack)

			if read_syn[1]:
				if read_syn[0] == "Ack Syn":
					print("Proper ack received, send ack back, then data/waiting for data")
					self.port = read_syn[3]
					window_size = read_syn[5]
					ack = read_syn[2] + len(syn_ack)

					self.sock.sendto(Packet.ack(self.seq_number, ack, args.p, self.port, window_size, syn=True).binary_combine(),
									 server_connection)

					if args.w:
						self.send_data(args.f, window_size, args.a, args.p, self.sock)
					else:
						self.receive_data(args.f, self.sock, args.p, window_size, ack, args.a)
				else:
					print("Improper ack received, please try connection again")
					self.sock.close()
					exit(0)
			else:
				print("Error in the checksum for ack syn, please try connection again")
				self.sock.close()
				exit(0)
		except socket.timeout:
			print("Connection time out, connection not established")
			exit(0)


if __name__ == '__main__':
	client = Client()
