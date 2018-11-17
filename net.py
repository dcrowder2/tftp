# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol
from socket import SOCK_STREAM
from socket import AF_INET
from socket import socket
import argparse
from packet import Packet
from file_reader import FileReader
import random


class Net:

	def __init__(self):
		self.parser = argparse.ArgumentParser(
			description='An implementation of TFTP following RFC1350, by Dakota Crowder.')
		self.parser.add_argument('-p', metavar='port number', type=int, help='The port for the server')
		self.sock = socket(AF_INET, SOCK_STREAM)
		# start with a random sequence number, in the range of 32 bits
		self.sequence_number = random.randint(0, 4294967295)

	def send_data(self, filename, WIN_SIZE):
		file_reader = FileReader(filename)
		# Pre-load file chunks with enough to fill the window at first
		file_chunks = file_reader.get_chunk(WIN_SIZE)
		# load in the first packets
		window = []
		for chunk in file_chunks:
			window.append(Packet.data(self.sequence_number, chunk))
			self.up_sequence_number(len(chunk))
			file_chunks.remove(chunk)

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
