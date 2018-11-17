import bitstring


# The parent to all packets
class Header:

	def __init__(self, write):
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
		self.source_port = bitstring.BitArray()
		self.destination_port = bitstring.BitArray()
		self.sequence_number = bitstring.BitArray()
		self.acknowledge_number = bitstring.BitArray()
		self.data_offset = bitstring.BitArray(5)
		self.reserved = bitstring.BitArray('0b000000')
		self.urgent_flag = bitstring.Bits(bin=0)
		self.acknowledge_flag = bitstring.Bits(bin=0)
		self.push_flag = bitstring.Bits(bin=0)
		self.reset_flag = bitstring.Bits(bin=0)
		self.synchronize_flag = bitstring.Bits(bin=0)
		self.final_flag = bitstring.Bits(bin=0)
		self.window_size = bitstring.BitArray()
		self.checksum = bitstring.BitArray()
		self.urgent_pointer = bitstring.BitArray('0b0000')

	def combine(self):
		complete = bitstring.BitArray()
		complete += self.source_port
		complete += self.destination_port
		complete += self.sequence_number
		complete += self.acknowledge_number
		complete += self.data_offset
		complete += self.reserved
		complete += self.urgent_flag
		complete += self.acknowledge_flag
		complete += self.push_flag
		complete += self.reset_flag
		complete += self.synchronize_flag
		complete += self.final_flag
		complete += self.window_size
		complete += self.checksum
		complete += self.urgent_pointer
		return complete
