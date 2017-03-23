import socket
import sys
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
from parseexception import ParseException

from Logger import Logger

import json

class Client:
	legal_methods = ['login <username>', 'logout', 'msg <message>', 'history', 'names', 'help']
	program_die = False
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
		
		self.run()

	def run(self):
		self.logger.message("""
\033[94m///////////////////////////////////////\033[0m
\033[94m//             SLACK v2.0            //\033[0m
\033[94m//\033[0m   Just like slack, only better!   \033[94m//\033[0m 
\033[94m///////////////////////////////////////\033[0m
""")

		# Initiate the connection to the server
		try: 
			self.connect()
			self.logger.success({
				'title': 'Connected to Chat',
				'message': 'Successfully connected to chat on address: {}:{}'.format(self.host, self.server_port)
			})
		except Exception as e:
			self.logger.error({'title': 'Connection Error', 'message': e})
			self.logger.message('\nExiting program\n')
			sys.exit(1)


		# N.B. This HAVE TO be after Socket has connected (ref. line 32)
		self.message_receiver = MessageReceiver(self, self.connection)
		self.message_receiver.start()

		while True:
			self.logger.message({
				'title': '\nCHOOSE YOUR ACTION', 
				'message': '  ' + '\n  '.join(self.legal_methods)
			})

			try:
				action = input('> ')
			except KeyboardInterrupt as keyey:
				self.logout()
				break

			# Kills the program if this is set to true
			if self.program_die:
				break

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
			raise ConnectionError('Could not connect to server at {}:{}'.format(self.host, self.server_port))


	def disconnect(self):
		# TODO: Handle disconnection
		self.logger.message({'title': 'Logged Out', 'message': 'Bye\n'})
		sys.exit(0)


	def receive_message(self, message):
		if message == 'DIE':
			self.logger.message('\nShutting down\n[press enter to exit]')
			self.program_die = True # Shuts the program down in the program-loop
			sys.exit(0) # Stops the thread (Remove and you'll get an segmentation fault on errors)
			
		try:
			self.logger.message( self.parser.parse(message) )
		except ParseException as e:
			# Use parse error to forward errors from the parser
			self.logger.error({'title': e.args[1], 'message': e.args[0]} if len(e.args) > 1 else str(e))

		print('\n>', end=" ") # Quick fix, so that the user knows what to see
		
		
	def send_payload(self, data):
		payload = json.dumps(data).encode()
		self.connection.sendall(payload)

		if data['request'] == 'logout':
			self.disconnect()


	def login(self):
		user = input('username > ')
		return { 'request': 'login', 'content': user }


	def logout(self):
		return { 'request': 'logout' }


	def names(self):
		return { 'request': 'names' }


	def history(self):
		return { 'request': 'history' }


	def msg(self):
		msg = input('message > ')
		return { 'request': 'msg', 'content': msg }


	def help(self):
		return { 'request': 'help'}


if __name__ == '__main__':
	"""
	This is the main method and is executed when you type "python Client.py"
	in your terminal.

	No alterations are necessary
	"""

	# A user can choose to use custom addresses
	# if not, the default 'localhost' and 9998 is used
	host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
	port = int(sys.argv[2]) if len(sys.argv) > 2 else 9998

	client = Client(host, port)
