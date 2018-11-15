# The parent to all packets, contains the op-code header
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
		self.source_port = bytearray()
		self.destination_port = bytearray()
		self.sequence_number = bytearray()
		self.acknowledge_number = bytearray()
		self.data_offset = bytearray(5)
		self.reserved = bytearray([0, 0, 0, 0, 0, 0])
		self.urgent_flag = 0
		self.acknowledge_flag = 0
		self.push_flag = 0
		self.reset_flag = 0
		self.synchronize_flag = 0
		self.final_flag = 0
		self.window_size = bytearray()
		self.checksum = bytearray()
		self.urgent_pointer = bytearray([0, 0, 0, 0])

	def combine(self):
		complete = bytearray()
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
