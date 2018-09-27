from socket import SOCK_STREAM
from socket import AF_INET
from socket import socket
import argparse


class Net:
	def __init__(self):
		self.parser = argparse.ArgumentParser(
			description='An implementation of TFTP following RFC1350, by Dakota Crowder.')
		self.parser.add_argument('-p', metavar='port number', type=int, help='The port for the server')
		self.sock = socket(AF_INET, SOCK_STREAM)


