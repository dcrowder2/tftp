from datack_packet import Datack
from error_packet import Error
from request_packet import Request


class Packet:

	@staticmethod
	def request(filename, mode, write_flag):
		if write_flag:
			new_packet = Request(2, filename, mode).packet
		else:
			new_packet = Request(1, filename, mode).packet
		return new_packet

	@staticmethod
	def data(block_number, data_line):
		new_packet = Datack(3, block_number).packet
		new_packet += bytearray(data_line)
		return new_packet

	@staticmethod
	def read_packet(packet):
		op_code = packet[1]
		return_info = []
		if op_code == 1 or op_code == 2:
			return_info.append(packet[1])
			return_info.append(packet[3])
		elif op_code == 3:
			# The block number is byte 3 and 4 of the packet, and should be added together to get the correct number
			return_info.append(packet[2] + packet[3])
			# Then the next part is the data chunk from the file
			return_info.append(packet[4:])
		elif op_code == 4:
			return_info.append(packet[1])
		else:
			return_info.append(packet[1])
		return return_info
