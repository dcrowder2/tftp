from datack_packet import Datack
from error_packet import Error
from request_packet import Request


class Packet:

	def __init__(self):
		self.block_number = 0

	def request(self, filename, mode):
		