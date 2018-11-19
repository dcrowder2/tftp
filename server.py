# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol
from net import Net
from packet import Packet
from os import path
from socket import socket
import random


class Server(Net):

	def __init__(self):
		# Run super initializer
		Net.__init__(self)

		# parse the arguments
		args = self.parser.parse_args()

		self.port = args.p()
		self.win_size = random.randint(4, 9)

		# bind the socket to the port
		self.sock.bind(('', args.p))

		print("Server IP: " + str(self.sock.getsockname()) + "\nPort number: " + str(args.p) + "\nWaiting for connection")
		while True:
			message, address = self.sock.recv(516)
			decoded_message = Packet.read_packet(message)
			# Kill packet received
			if decoded_message[0] == 'end':
				self.sock.close()
				exit(0)

			if decoded_message[1]:
				if decoded_message[0] == "Syn":
					print("Connection requested from " + str(address))
					print("Sending syn ack...")
					ack = decoded_message[2]
					write_flag = decoded_message[3]
					filename = decoded_message[4]
					self.sock.sendto(Packet.ack(self.seq_number, ack, address[1], self.port, self.win_size, syn=True),
																												address)
					self.sock.settimeout(.5)
					try:
						message, address = self.sock.recvfrom(1472)
						decoded_message = Packet.read_packet(message)

						if decoded_message[1]:
							if decoded_message[0] == "Ack Syn":
								print("Three way handshake confirmed")

								if write_flag:
									# Since a file added to the server will be preappended with 'new', this needs to be checked as well
									if path.exists(filename) or path.exists('new'+filename):
										print("Trying to send a file that already exists, sending error, closing "
												"connection")
										return_packet = Packet.error(6, address[1], self.port, self.seq_number)
										self.sock.sendto(return_packet, address)
									else:
										print("Ready to receive data...")
										Net.receive_data(self, "new" + filename, self.sock, address[1], self.win_size,
																										ack, address[0])
								else:
									if path.exists('new' + filename):
										pathname = 'new' + filename
									else:
										pathname = filename
									# Sending a file not found error, this is redundant check if there is a 'new' + filename but if there
									#  isn't one this one checks for the original name
									if not path.exists(pathname):
										print("trying to send a file that doesn't exist, sending error, closing "
												"connection")
										send_packet = Packet.error(1, address[1], self.port, self.seq_number)
										self.sock.sendto(send_packet, address)
									else:
										print("Sending data...")
										Net.send_data(self, pathname, self.win_size, address[0], address[1], self.sock)
					except socket.timeout as e:
						print("Syn ack timeout, connection refused")


if __name__ == '__main__':
	server = Server()

