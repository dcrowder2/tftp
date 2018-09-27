from datack import Datack
from error import Error
from request import Request


class Packet:

	def __init__(self):
		self.block_number = 0

	def request(self, filename, mode):
		