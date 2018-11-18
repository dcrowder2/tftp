# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol
from datack_packet import Datack
from error_packet import Error
from request_packet import Request
import random
from bitstring import Bits


class Packet:

	@staticmethod
	def corrupt(packet):
		d100_roll = random.randint(0, 100)
		if d100_roll <= 5:
			# To corrupt the checksum I set it to the binary representation for the word no, which is 16 bits,
			# and while it is possible for the checksum to be this, it is very slim chances so it should be fine
			packet.checksum = Bits(b'No')

	@staticmethod
	def request(filename, write_flag, d_port, s_port, seq_num):
		if write_flag:
			new_packet = Request(2, filename, seq_num, s_port, d_port)
		else:
			new_packet = Request(1, filename, seq_num, s_port, d_port)
		# after initialization checksum needs to be calculated
		new_packet.calc_checksum()
		# and we return the bitarray for the packet
		return new_packet.combine()

	@staticmethod
	def data(sequence_number, data_line, s_port, d_port, ack_num, fin=False):
		new_packet = Datack(3, sequence_number, ack_num, d_port, s_port, data_line, fin=fin)
		new_packet.calc_checksum()
		# Data packets are to be corrupted with a 5% probability, so we need to roll the die
		Packet.corrupt(new_packet)
		return new_packet.combine()

	@staticmethod
	def error(error_code, d_port, s_port, seq_num, in_message=''):
		new_packet = Error(error_code, d_port, s_port, seq_num, in_message)
		new_packet.calc_checksum()
		return new_packet.combine()

	@staticmethod
	def ack(sequence_number):
		return Datack(4, sequence_number)

	@staticmethod
	def kill():
		return bytearray([0, 9])

	@staticmethod
	def read_packet(packet):
		op_code = packet[1]
		return_info = []
		# A Read(1) or Write(2) Request
		if op_code == 1 or op_code == 2:
			# Add flag for if write then true, if read then false
			return_info.append(op_code == 2)
			# getting the file name
			index = Packet.find_zero(packet[2:])
			return_info.append(packet[2:index].decode('utf-8'))
			# getting the mode
			last = Packet.find_zero(packet[(index + 1):])
			return_info.append(packet[index + 1: index + last - 1].decode('utf-8'))
		# Data packet
		elif op_code == 3:
			# The block number is byte 3 and 4 of the packet, and should be added together to get the correct number
			return_info.append((packet[2] << 8) | packet[3])
			# Then the next part is the data chunk from the file
			return_info.append(packet[4:])
		# Ack packet
		elif op_code == 4:
			return_info.append((packet[2] << 8) | packet[3])
		# Kill Packet
		elif op_code == 9:
			return_info.append('end')
		# Error packet
		else:
			print("Error number " + str(packet[3]) + ": " + packet[4:-1].decode('utf-8'))
			exit(0)
		return return_info
