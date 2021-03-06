# -*- coding: utf-8 -*-
import socketserver
import socket
import json
import re
import time
from models.history import History
from models.names import Names


threads=[]
"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

class ClientHandler(socketserver.BaseRequestHandler):
	"""
	This is the ClientHandler class. Everytime a new client connects to the
	server, a new ClientHandler object will be created. This class represents
	only connected clients, and not the server itself. If you want to write
	logic for the server, you must write it outside this class
	"""

	def handle(self):
		self.possible_responses = {
				'login': self.login,
				'logout': self.logout,
				'msg':self.msg,
				'names':self.names,
				'help': self.help,
				'history': self.history
			}

		self.logged_in = False
		self.name = None
		self.history_mod = History("messages.json")
		self.names_mod = Names('db.json')
		
		self.ip = self.client_address[0]
		self.port = self.client_address[1]
		self.connection = self.request

		threads.append(self)

		# Loop that listens for messages from the client
		while True:
			received_string = self.connection.recv(4096)

			payload = json.loads(received_string.decode())

			if payload['request'] in self.possible_responses:
				self.possible_responses[payload['request']](payload)
			else:
				self.error("Illegal request {}".format(payload['request']))


	def send(self, content, response):
		message = json.dumps( self.history_mod.render_message(self.name, content, response) )
		self.connection.sendall(message.encode())
		

	def login(self, payload):
		if self.logged_in:
			return self.error("You're already logged in")
		
		if not re.match('^[A-Za-z0-9]+$',payload["content"]):
			return self.error('Bad username')
		
		self.name = payload["content"]
		
		if self.names_mod.findOne(self.name):
			return self.error('Username is already taken')

		user = self.names_mod.append(self.name)		
		self.logged_in = True
		
		# Create response payload
		msg = self.history_mod.render_message('server', 'User: {} has logged in'.format(self.name), 'info')

		# Inform all threads of a new user
		for i in threads:
			try:
				i.connection.sendall(json.dumps(msg).encode())
			except OSError as ose:
				print(i)
				print(ose)

		# Respond to user with the chat history
		self.history(payload)
		

	def logout(self, payload):
		if not self.logged_in:
			self.error("You're not logged in, you broke the system (Thanks obama)")
			return

		try:
			self.names_mod.remove(self.name)
		except IOError as ioe:
			print(ioe)
			
		msg = self.history_mod.render_message('server', '{} has logged out'.format(self.name), 'info')

		for i in threads:
			try:
				i.connection.sendall(json.dumps(msg).encode())
			except OSError as ose:
				print(i)
				print(ose)
			
		threads.remove(self)
			
		self.logged_in = False
		self.name = None
		self.connection.close()


	def msg(self, payload):
		if not self.logged_in:
			self.error("You're not logged in")
			return

		msg = self.history_mod.append(self.name, payload["content"])
			
		for i in threads:
			try:
				i.connection.sendall(json.dumps(msg).encode())
			except OSError as ose:
				print(i)
				print(ose)	


	def names(self,payload):
		if(not self.logged_in):
			return self.error("You're not logged in")
		
		self.send(json.dumps(self.names_mod.find()), 'names')
			
					
	def history(self, payload):
		if(not self.logged_in):
			return self.error("You're not logged in")
		
		self.send(json.dumps(self.history_mod.find()), 'history')

	
	def help(self, payload):
		with open("help.txt", "r") as f:
			helpstr = f.read()
			self.send(helpstr, "info")


	def error(self, something):
		self.send(something, "error")
		

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	"""
	This class is present so that each client connected will be ran as a own
	thread. In that way, all clients will be served by the server.

	No alterations are necessary
	"""
	allow_reuse_address = True
	

if __name__ == "__main__":
	"""
	This is the main method and is executed when you type "python Server.py"
	in your terminal.

	No alterations are necessary
	"""
	HOST, PORT = 'localhost', 9998
	print ('Server running...')

	# Set up and initiate the TCP server
	server = ThreadedTCPServer((HOST, PORT), ClientHandler)
	server.serve_forever() #You will serve forever SLAVE!
