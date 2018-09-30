from socket import SOCK_STREAM
from socket import AF_INET
from socket import socket
import argparse
from packet import Packet
from file_reader import FileReader
from os import path


class Net:

	def __init__(self):
		self.parser = argparse.ArgumentParser(
			description='An implementation of TFTP following RFC1350, by Dakota Crowder.')
		self.parser.add_argument('-p', metavar='port number', type=int, help='The port for the server')
		self.sock = socket(AF_INET, SOCK_STREAM)

	def send_data(self, filename, sock):
		# Loading the chunks of 512 bytes
		file_chunks = FileReader.read(filename)
		# the last chunk need to be less than 512, if not then another packet needs to be sent
		last_chunk = len(file_chunks)
		block_number = 1

		for chunk in file_chunks:

			send_packet = Packet.data(block_number, chunk)
			sock.send(send_packet)

			receive_ack = Packet.read_packet(sock.recv(516))

			# if the ack is not the block number sent, then a error packet is sent and the connection is closed
			if receive_ack[0] != block_number:
				send_packet = Packet.error(0, 'Incorrect acknowledgment, closing connection')
				sock.send(send_packet)
				sock.close()
				exit(0)

			block_number += 1

		# Sending the last empty packet so the receiver knows it is finished if the last packet is 512
		if len(file_chunks[last_chunk-1]) == 512:
			send_packet = Packet.data(block_number, b'')
			sock.send(send_packet)

	def receive_data(self, filename, sock):
		write_file = open('new' + filename, 'wb')
		last_packet = False

		while not last_packet:
			receive_packet = sock.recv(516)

			data = Packet.read_packet(receive_packet)
			# A check if the last packet is empty
			if len(data[1]) == 0:
				print('nah')
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
