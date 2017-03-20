# -*- coding: utf-8 -*-
import socketserver
import socket
import json
import re
import time

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
			# More key:values pairs are needed  
			}
		self.loggedin=False
		self.name=None

		"""
		This method handles the connection between a client and the server.
		"""

		self.ip = self.client_address[0]
		self.port = self.client_address[1]
		self.connection = self.request

		# Loop that listens for messages from the client
		while True:

			received_string = self.connection.recv(4096)

			payload=json.loads(received_string.decode())

			if(received_string.decode=="quit"):
				self.logout(payload)

			if payload['request'] in self.possible_responses:
				# Mulig return dreper pipen
				# Ja det gjorde den
				self.possible_responses[payload['request']](payload)
			else:
				self.error(payload)


	def createResponse(self, content, response):
		message = json.dumps({"timestamp": time.time(), "sender": self.name, "response": response, "content": content})
		self.connection.sendall(message.encode())

	def login(self, payload):
		if self.loggedin:
			return self.history(payload)
		
		if not re.match('[a-zA-Z0-9]', payload["content"]):
			return self.createResponse('Bad username', 'error')
			
		self.name = payload["content"]
		
		user = {
			'username': payload['content'], 
			'lastlogin': str(time.time())
		}
			
		with open('db.json', 'r+') as f:
			a=f.read()
			a = a if len(a) > 0 else '[]'
			print(a)
			names = json.loads(a)
			print(names)
			self.name = payload['content']
			names.append(user)
			#print(names)
			f.seek(0)
			f.truncate()
			f.write(json.dumps(names))
			self.history(payload)

		

	def logout(self, payload):
		if(self.loggedin):
			with open("db.json","r+") as f:
				temp=json.loads(f.read())
				try:
					i = list(filter(lambda p: p["username"] == self.name, temp))[0]
					
					temp.remove(i)
					f.seek(0)
					f.truncate()
					f.write(json.dumps(temp))
					
					self.loggedin = False
					self.connection.close()
				except:
					print("username does not exist")
				finally:
					return
		else:
			self.error(payload)


	def msg(self, payload):
		if(self.loggedin):
			with open("messages.json", "r+") as f:
				a=f.read()
				a = a if len(a) > 0 else '[]'
				temp=json.load(a)
				temp.append({"username":self.name, "message":payload['content'], 'timestamp':time.time()})
				f.seek(0)
				f.truncate()
				f.write(json.dumps(temp))
				self.history(payload)
		else:
			self.error(payload)


	

	def names(self,payload):
		with open("db.json") as f:
			a=f.read()
			
			self.createResponse(a,"names")
			print("hei")

				
			

	
	def history(self, payload):
		with open("messages.json") as f:
		
			self.createResponse(f.read(),"messages")

		

	def help(self, payload):
		# TODO - place in help.txt
		helpstr="""\n
		##############################################
		#               Slack v2.0 HELP              #
		##############################################
		Slack v2.0 is a Command Line Interface (CLI) chatting application, with simple
		authentication.

		To get into the action, you the user only has to 'login' with a valid username 
		(large or small letters and numbers)




		"""
		createResponse(helpstr,"help")

		

	def error(self, payload):


		self.createResponse("Something went wrong","error")
		


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
	server.serve_forever()
