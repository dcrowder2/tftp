# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol
from header import Header
from error_packet import Error
import bitstring


# This class encompasses the duties for a data packet and a ack packet
class Datack(Header):

	def __init__(self, in_code, block_number, data):

		Header.__init__(self, in_code)

