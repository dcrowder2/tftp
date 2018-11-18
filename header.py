import bitstring


# The parent to all packets
# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol

# The parent to all packets, contains the op-code header
class Header:

	def __init__(self, seq_num, s_port, d_port, ack_num=0, win_size=0, write=False, syn=False, ack=False, fin=False):
		"""                 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 3 3
		0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
		+-------------------------------+-------------------------------+
		|          Source Port          |       Destination Port        |
		+-------------------------------+-------------------------------+
		|                       Sequence Number                         |
		+---------------------------------------------------------------+
		|                      Acknowledge Number                       |
		+-------+-----+-+-+-+-+-+-+-+-+-+-------------------------------+
		|  Data |           |U|A|P|R|S|F|                               |
		| Offset|  Reserved |R|C|S|S|Y|I|          Window Size          |
		|       |           |G|K|H|T|N|N|                               |
		+-------+-----+-+-+-+-+-+-+-+-+-+-------------------------------+
		|           Checksum            |  Urgent Pointer (if URG set)  |
		+-------------------------------+-------------------------------+
		"""
		# Getting the length of all the numbers, because if it is less than 16 or 32 bits as determined from above
		# they need to have those zeros append to the front, so we need the length, which when you get the length of
		# the number as represented in binary, it would be '0b0' for zero, which is length 3, but should be length 1,
		#  so the '0b' needs to be sliced off
		len_source = len(bin(s_port)[2:])
		len_dest = len(bin(d_port)[2:])
		len_ack = len(bin(ack_num)[2:])
		len_seq = len(bin(seq_num)[2:])
		len_win = len(bin(win_size)[2:])

		# If the length of source is less than 16 it needs the zeros appended to them, same with all of the if
		# statements
		if len_source < 16:
			# calling BitArray with a number creates an array with that many zeros
			self.source_port = bitstring.BitArray(16 - len_source)
			# then you append the binary representation to the end of the array
			self.source_port.append(bin(s_port))
		elif len_source == 16:
			self.source_port = bitstring.BitArray(bin=bin(s_port))
		# Same as source_port
		if len_dest < 16:
			self.destination_port = bitstring.BitArray(16 - len_dest)
			self.destination_port.append(bin(s_port))
		elif len_dest == 16:
			self.destination_port = bitstring.BitArray(bin=bin(d_port))
		# Same as source_port
		if len_seq < 32:
			self.sequence_number = bitstring.BitArray(32 - len_seq)
			self.sequence_number.append(bin(seq_num))
		elif len_seq == 32:
			self.sequence_number = bitstring.BitArray(bin=bin(seq_num))
		# Same as source_port
		if len_ack < 32:
			self.acknowledge_number = bitstring.BitArray(32 - len_ack)
			self.acknowledge_number.append(bin(ack_num))
		elif len_ack == 32:
			self.acknowledge_number = bitstring.BitArray(bin=bin(ack_num))

		# no options so always a offset of 5 words
		self.data_offset = bitstring.BitArray('0b0101')
		self.reserved = bitstring.BitArray(6)
		# Urgent will be used as read/write bit
		self.urgent_flag = bitstring.Bits(bin(write))

		self.acknowledge_flag = bitstring.Bits(bin(ack))
		self.push_flag = bitstring.Bits(bin(0))
		self.reset_flag = bitstring.Bits(bin(0))

		self.synchronize_flag = bitstring.Bits(bin(syn))

		self.final_flag = bitstring.Bits(bin(fin))
		# Same as source_port
		if len_win < 16:
			self.window_size = bitstring.BitArray(16 - len_win)
			self.window_size.append(bin(win_size))
		elif len_win == 16:
			self.window_size = bitstring.BitArray(bin=bin(win_size))
		# Checksum needs to be zeros for the calculation for checksum
		self.checksum = bitstring.BitArray(16)
		self.urgent_pointer = bitstring.BitArray(16)

	def combine(self):
		complete = bitstring.BitArray()
		complete.append(self.source_port)
		complete.append(self.destination_port)
		complete.append(self.sequence_number)
		complete.append(self.acknowledge_number)
		complete.append(self.data_offset)
		complete.append(self.reserved)
		complete.append(self.urgent_flag)
		complete.append(self.acknowledge_flag)
		complete.append(self.push_flag)
		complete.append(self.reset_flag)
		complete.append(self.synchronize_flag)
		complete.append(self.final_flag)
		complete.append(self.window_size)
		complete.append(self.checksum)
		complete.append(self.urgent_pointer)
		return complete

	# To be overridden for any packet that has data (data, read, write, error)
	# This uses the calculation described in RFC 793, which is the one's complement of the sum of the one's
	# compliments of the 16 bit words in the packet, which is just splitting the packet up into 16 bit sections
	def calc_checksum(self):
		all_words = self.combine()
		end_of_word = 16
		summation = (~all_words[:end_of_word]).uint

		for i in range((len(all_words)//16) - 1):
			start_of_word = end_of_word
			end_of_word += 16
			summation += (~all_words[start_of_word:end_of_word]).uint
		# If there is more bits that are a full word we need to add them as well
		if len(all_words[end_of_word:]) > 0:
			final_word = bitstring.BitArray(16 - len(all_words[end_of_word:]))
			final_word.append(all_words[end_of_word:])
			summation += (~final_word).uint

		bin_sum = bitstring.Bits(bin(summation))

		while len(bin_sum) > 16:
			over_hang = bin_sum[:(len(bin_sum)-16)].uint
			left_over = bin_sum[(len(bin_sum)-16):].uint
			bin_sum = bitstring.Bits(bin(over_hang + left_over))

		if len(bin_sum) < 16:
			temp_sum = bitstring.BitArray(16 - len(bin_sum))
			temp_sum.append(bin_sum)
			bin_sum = temp_sum
		self.checksum = ~bin_sum
