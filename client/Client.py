import socket
import sys
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

from Logger import Logger

import json

class Client:
	legal_methods = ['login <username>', 'logout', 'msg <message>', 'history', 'names', 'help']

	"""
	This is the chat client class
	"""
	def __init__(self, host, server_port):
		"""
		This method is run when creating a new Client object
		"""
		self.host = host
		self.server_port = server_port
		self.logger = Logger(None)
		self.parser = MessageParser()

		# Set up the socket connection to the server
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		# TODO: Finish init process with necessary code
		self.run()

	def run(self):
		# Initiate the connection to the server
		try: 
			self.connect()
		except Exception as e:
			self.logger.error({'title': 'Connection Error', 'message': e})
			sys.exit(1)

		# N.B. This HAVE TO be after Socket has connected (ref. line 32)
		self.message_receiver = MessageReceiver(self, self.connection)
		self.message_receiver.start()

		while True:
			print('--- Choose action ---')
			print('\t' + '\n\t'.join(self.legal_methods))
			action = input('> ').strip()

			method = None # Stores the selected methods
			if action == 'login':
				method = self.login
			elif action == 'logout':
				method = self.logout
			elif action == 'names':
				method = self.names
			elif action == 'history':
				method = self.history
			elif action == 'msg':
				payload = input('message: ')
				method = self.msg
			elif action == 'help':
				method = self.help
			else:
				self.logger.error({
					'title': 'Illegal action', 
					'message': 'action: {}'.format(action)
				})
				continue

			try:
				self.send_payload(method())
			except Exception as e:
				self.logger.error({'title': 'Sending Error', 'message': e})
			
	
	def connect(self):
		"""
		Centralizes the connection process
		"""
		try:
			self.connection.connect((self.host, self.server_port))
		except ConnectionRefusedError as e:
			raise Error('Could not connect to server at {}:{}'.format(self.host, self.server_port))


	def disconnect(self):
		# TODO: Handle disconnection
		print('disconnect')


	def receive_message(self, message):
		self.logger.message(self.parser.parse(message))
		

	def send_payload(self, data):
		payload = json.dumps(data).encode()
		self.connection.sendall(payload)


	def login(self):
		user = input('username: ')
		return { 'request': 'login', 'content': user }


	def logout(self):
		return { 'request': 'logout' }


	def names(self):
		return { 'request': 'names' }


	def history(self):
		return { 'request': 'history' }


	def msg(self):
		msg = input('message: ')
		return { 'request': 'msg', 'content': msg }


	def help(self):
		return { 'requests': 'help'}


if __name__ == '__main__':
	"""
	This is the main method and is executed when you type "python Client.py"
	in your terminal.

	No alterations are necessary
	"""
	client = Client('localhost', 9998)