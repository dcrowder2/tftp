# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol
from socket import SOCK_DGRAM, AF_INET, socket
import argparse
from packet import Packet
from file_reader import FileReader
import random
from window import Window


class Net:

	def __init__(self):
		self.parser = argparse.ArgumentParser(
			description='An implementation of TFTP following RFC1350, by Dakota Crowder.')
		self.parser.add_argument('-p', metavar='port number', type=int, help='The port for the server')
		self.sock = socket(AF_INET, SOCK_DGRAM)
		# start with a random sequence number, in the range of 32 bits
		self.sequence_number = random.randint(0, 4294967295)
		# this is not correct, it needs to be updated when a connection is made, but needs to be defined here,
		# so it can be used in send_data
		self.port = 0

	def send_data(self, filename, win_size, d_address, d_port, sock_to_send):
		file_reader = FileReader(filename)
		# Pre-load file chunks with enough to fill the window at first
		file_chunks = file_reader.get_chunk(win_size)
		# load in the first packets
		window = Window(win_size)
		packets = []

		for chunk in file_chunks:
			packets.append(Packet.data(self.sequence_number, chunk, self.port, d_port))
			self.up_sequence_number(len(chunk))

		window.add_packets(packets)
		print("Sending first window...")
		window.send(sock_to_send, d_address, d_port)

		done = False

		while not done:
			sock_to_send.settimeout(.5)
			try:
				print("Waiting for ack...")
				message, address = sock_to_send.recvfrom(1472)
				ack_packet = Packet.read_packet(message)
				# checking valid checksum
				if ack_packet[1]:
					# adding packets into the window to be sent
					if ack_packet[0] == 'ack':
						print("Ack received")

						window.remove_packets(ack_packet[2])

						file_chunks = file_reader.get_chunk(window.get_packet_space())

						# removing empty chunks if they are present
						if file_chunks[-1] == b'':
							file_chunks = list(filter(None, file_chunks))
							# after removing all the empty chunks, add one more blank if the last packet is exactly 1452
							if len(file_chunks[-1]) == 1452:
								file_chunks.append(b'')

						packets = []

						for chunk in file_chunks:
							if len(chunk) == 1452:
								packets.append(Packet.data(self.sequence_number, chunk, self.port, d_port))
								self.up_sequence_number(len(chunk))
							else:
								packets.append(Packet.data(self.sequence_number, chunk, self.port, d_port, fin=True))
								done = True

						window.add_packets(packets)

						window.send(sock_to_send, d_address, d_port)
					# If the ack packet is instead an error packet, print error and resend
					elif ack_packet[0] == 'Err':
						print("Error returned: " + ack_packet[2] + " " + ack_packet[3])
						print("\nResending...")
						window.send(sock_to_send, d_address, d_port)
				else:
					error_packet = Packet.error(0, d_port, self.port, self.sequence_number, in_message="Checksum error")
					sock_to_send.sendto(error_packet)
					self.up_sequence_number(len(error_packet))
			except socket.timeout as e:
				print("Receiving ack timeout, resending...")
				window.send(sock_to_send, d_address, d_port)



	def receive_data(self, filename, sock):
		write_file = open('new' + filename, 'wb')
		last_packet = False

		while not last_packet:
			receive_packet = sock.recv(516)

			data = Packet.read_packet(receive_packet)
			# A check if the last packet is empty
			if len(data[1]) == 0:
				send_packet = Packet.ack(data[0])
				sock.send(send_packet)
				break

			write_data = data[1]
			write_file.write(write_data)

			send_packet = Packet.ack(data[0])
			sock.send(send_packet)

			# If the last packet is not empty but less then 512 bytes
			if len(data[1]) < 512:
				last_packet = True

	# The Sequence number can only go up to 32 bites in size, so it needs to wrap around
	def up_sequence_number(self, addend):
		if self.sequence_number + addend >= 4294967295:
			self.sequence_number = 0
			self.sequence_number += (self.sequence_number + addend) - 4294967295
		else:
			self.sequence_number += addend
