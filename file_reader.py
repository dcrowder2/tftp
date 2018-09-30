# Dakota Crowder
# CSCE A365 Computer Networks
# University of Alaska Anchorage
# Trivial File Transport Protocol

class FileReader:

	@staticmethod
	def read(filename):
		file = open(filename, 'rb')
		broken_up = []
		chunk = file.read(512)
		while chunk:
			broken_up.append(chunk)
			chunk = file.read(512)
		return broken_up
