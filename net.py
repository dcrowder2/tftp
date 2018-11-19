# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol
from socket import SOCK_DGRAM, AF_INET, socket
import socket
import argparse
from packet import Packet
from file_reader import FileReader
import random
from window import Window
from bitstring import BitArray


class Net:

	def __init__(self):
		self.parser = argparse.ArgumentParser(
			description='An implementation of TFTP following RFC1350, by Dakota Crowder.')
		self.parser.add_argument('-p', metavar='port number', type=int, help='The port for the server')
		self.sock = socket.socket(AF_INET, SOCK_DGRAM)
		# start with a random sequence number, in the range of 32 bits
		self.seq_number = random.randint(0, 4294967295)
		# this is not correct, it needs to be updated when a connection is made, but needs to be defined here,
		# so it can be used in send_data
		self.port = 0

	def re_sock(self):
		self.sock = socket.socket(AF_INET, SOCK_DGRAM)

	def send_data(self, filename, win_size, d_address, d_port, sock_to_send):
		file_reader = FileReader(filename)
		# Pre-load file chunks with enough to fill the window at first
		file_chunks = file_reader.get_chunk(win_size)
		# load in the first packets
		window = Window(win_size)
		packets = []

		for chunk in file_chunks:
			packets.append(Packet.data(self.seq_number, chunk, self.port, d_port))
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
				print("Packet received, checking...")
				# checking valid checksum
				if ack_packet[1]:
					# adding packets into the window to be sent
					if ack_packet[0] == 'Ack':
						print("Ack received")
						window.remove_packets(ack_packet[2])

						file_chunks = file_reader.get_chunk(window.get_packet_space())

						# removing empty chunks if they are present
						if file_chunks[-1] == b'':
							file_chunks = list(filter(None, file_chunks))
							# after removing all the empty chunks, add one more blank if the last packet is exactly 1452
							if file_chunks:
								if len(file_chunks[-1]) == 1452:
									file_chunks.append(b'')
							else:
								file_chunks.append(b'')

						packets = []

						for chunk in file_chunks:
							if len(chunk) == 1452:
								packets.append(Packet.data(self.seq_number, chunk, self.port, d_port))
								self.up_sequence_number(len(chunk))
							else:
								packets.append(Packet.data(self.seq_number, chunk, self.port, d_port, fin=True))
								print("final packet created")
								print(packets[-1].sequence_number)
								done = True

						window.add_packets(packets)

						window.send(sock_to_send, d_address, d_port)
					# If the ack packet is instead an error packet, print error, dropped acked packets, then resend
					elif ack_packet[0] == 'Err':
						print("Error returned: " + str(ack_packet[2]) + " " + str(ack_packet[3]))
						print("Fixing checksums, moving acked packets out of window, and resending...")
						window.re_checksum()
						window.remove_packets(ack_packet[4], error=True)
						if window.get_packet_space() > 0:
							file_chunks = file_reader.get_chunk(window.get_packet_space())
							# removing empty chunks if they are present
							if file_chunks[-1] == b'':
								file_chunks = list(filter(None, file_chunks))
								# after removing all the empty chunks, add one more blank if the last packet is exactly 1452
								if file_chunks:
									if len(file_chunks[-1]) == 1452:
										file_chunks.append(b'')
								else:
									file_chunks.append(b'')

							packets = []

							for chunk in file_chunks:
								if len(chunk) == 1452:
									packets.append(Packet.data(self.seq_number, chunk, self.port, d_port))
									self.up_sequence_number(len(chunk))
								else:
									packets.append(Packet.data(self.seq_number, chunk, self.port, d_port, fin=True))
									done = True

							window.add_packets(packets)
						window.send(sock_to_send, d_address, d_port)
				else:
					error_packet = Packet.error(0, d_port, self.port, self.seq_number, in_message="Checksum error")
					sock_to_send.sendto(error_packet.binary_combine(), d_address)
					self.up_sequence_number(len(error_packet))
			except socket.timeout as e:
				print("Receiving ack timeout, resending...")
				window.send(sock_to_send, d_address, d_port)
	
		sock_to_send.settimeout(2)
		final_packet_received = False
		while not final_packet_received:
			try:
				final_packet, address = sock_to_send.recvfrom(1472)
				final_info = Packet.read_packet(final_packet)
				if final_info[1]:
					if final_info[0] == "Ack":
						window.remove_packets(final_info[2])
						if window.get_packet_space() == win_size:
							print("Final ack received, closing connection")
							sock_to_send.close()
							final_packet_received = True
						else:
							print("Final ack not received, sending whats left")
							window.send(sock_to_send, d_address, d_port)
			except socket.timeout as e:
				print("Final ack timed out, trying to resend")
				window.send(sock_to_send, d_address, d_port)

	def receive_data(self, filename, sock, d_port, win_size, start_ack, d_address):
		write_file = open('new' + filename, 'wb')
		last_packet = False
		MAX_RETRIES = 5

		ack = start_ack

		while not last_packet:
			error_flag = False
			retries = 0
			packets = []
			# Receiving the full window
			for i in range(win_size):
				sock.settimeout(2)
				try:
					print("Getting packet " + str(len(packets)) + " from the sender")
					receive_packet, address = sock.recvfrom(1472)
					packets.append(receive_packet)

				except socket.timeout as e:
					if len(packets) == 0:
						if retries < MAX_RETRIES:
							print("Receive timeout, retry: " + str(retries))
							retries += 1
						else:
							print("Max retries reached, closing connection")
							sock.close()
			if packets:
				for packet in packets:
					data = Packet.read_packet(packet)
					if data[1]:
						if data[0] == "Data":
							if data[2] == ack:
								print("Proper data packet received, writing data..." + str(data[2]))
								write_data = data[3].tobytes()
								write_file.write(write_data)
								ack = Net.up_ack(ack, len(BitArray(packet)))
								print("New ack :" + str(ack))
							else:
								print("Improper sequence number received, dumping improper packets" + str(data[2]))
								packets.clear()
						elif data[0] == "Fin":
							if data[2] == ack:
								print("Final packet received, writing, acking, then closing connection")
								write_file.write(data[3].tobytes())
								ack = Net.up_ack(ack, len(BitArray(packet)))
								last_packet = True

					else:
						print("Error detected, creating error packet, dumping packets")
						send_packet = Packet.error(0, d_port, self.port, self.seq_number, ack_num=ack, in_message="Checksum error")
						error_flag = True
						packets.clear()
						self.up_sequence_number(len(send_packet.binary_combine()))
				if not error_flag:
					send_packet = Packet.ack(self.seq_number, ack, d_port, self.port, win_size)

				print("Sending ack packet " + str(ack))
				sock.sendto(send_packet.binary_combine(), (d_address, d_port))
			else:
				print("No packets received, closing connection")
				sock.close()

	# The Sequence number can only go up to 32 bites in size, so it needs to wrap around
	def up_sequence_number(self, addend):
		if self.seq_number + addend >= 4294967295:
			self.seq_number = (self.seq_number + addend) - 4294967295
		else:
			self.seq_number += addend

	@staticmethod
	def up_ack(ack, addend):
		new_ack = ack
		proper_addend = (addend // 8) - 20
		if ack + proper_addend >= 4294967295:
			new_ack = (ack + proper_addend) - 4294967295
		else:
			new_ack += proper_addend
		return new_ack
