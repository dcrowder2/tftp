# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol
from datack_packet import Datack
from error_packet import Error
from request_packet import Request
import random
from bitstring import Bits, BitArray


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
	def ack(sequence_number, ack_number, d_port, s_port, win_size):
		return Datack(4, sequence_number, ack_number, d_port, s_port, win_size=win_size)

	@staticmethod
	def kill():
		return bytearray([0, 9])

	@staticmethod
	def check_checksum(checksum, packet):
		all_words = packet[:128]
		# removing the checksum from the packet for the calculation of the checksum, since it wasn't in the original
		# calculation for the checksum
		all_words.append(Bits('0b0000000000000000'))
		end_of_word = 16
		summation = (~all_words[:end_of_word]).uint

		for i in range((len(all_words) // 16) - 1):
			start_of_word = end_of_word
			end_of_word += 16
			summation += (~all_words[start_of_word:end_of_word]).uint
		# If there is more bits that are a full word we need to add them as well
		if len(all_words[end_of_word:]) > 0:
			final_word = BitArray(16 - len(all_words[end_of_word:]))
			final_word.append(all_words[end_of_word:])
			summation += (~final_word).uint

		bin_sum = Bits(bin(summation))

		while len(bin_sum) > 16:
			over_hang = bin_sum[:(len(bin_sum) - 16)].uint
			left_over = bin_sum[(len(bin_sum) - 16):].uint
			bin_sum = Bits(bin(over_hang + left_over))

		if len(bin_sum) < 16:
			temp_sum = BitArray(16 - len(bin_sum))
			temp_sum.append(bin_sum)
			bin_sum = temp_sum
		calculated_checksum = ~bin_sum

		return calculated_checksum == checksum

	@staticmethod
	def read_packet(packet):
		# if the packet is less than the length of the header, then it has to be a kill packet, so send the end signal
		if len(packet) < 20:
			return "end"

		source_port = packet[:16].uint
		dest_port = packet[16:32].uint
		sequence_number = packet[32:64].uint
		acknowledge_number = packet[64:96].uint
		data_offset = packet[96:100].uint
		write_flag = packet[106].bool
		ack_flag = packet[107].bool
		syn_flag = packet[110].bool
		fin_flag = packet[111].bool
		window_size = packet[112:128].uint
		checksum = packet[128:144]
		valid_checksum = Packet.check_checksum(checksum, packet)
