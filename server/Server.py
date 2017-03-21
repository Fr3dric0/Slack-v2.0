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
				self.error("impossible request")


	def createResponse(self, content, response):
		message = json.dumps({"timestamp": time.time(), "sender": self.name, "response": response, "content": content})
		self.connection.sendall(message.encode())

	def login(self, payload):
		if self.loggedin:
			return self.error("You're already logged in")
		
		if not re.match('[a-zA-Z0-9]', payload["content"]):
			return self.error('Bad username')
			
		self.name = payload["content"]
		
		user = {
			'username': payload['content'], 
			'lastlogin': str(time.time())
		}
			
		with open('db.json', 'r+') as f:
		
			a=f.read()
			a = a if len(a) > 0 else '[]'
			
			names = json.loads(a)


			if(len(list(filter(lambda p: p["username"] == self.name, names)))):
				
				self.loggedin=True
				names.append(user)
				#print(names)
				f.seek(0)
				f.truncate()
				f.write(json.dumps(names))
				with open("messages.json", "r+") as f:
					a=f.read()
					print(a)
					print("hei")
					a = a if len(a) > 0 else '[]'
					temp=json.loads(a)
					temp.append({"username":"", "message":self.username+" has logged in", 'timestamp':time.time()})
					print(temp)
					f.seek(0)
					f.truncate()
					f.write(json.dumps(temp))
					self.history(payload)
			else:
				self.error("Username taken")
		
				

		

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
			self.error("You're not logged in, you broke the system (Thanks obama)")


	def msg(self, payload):
		if(self.loggedin):
			with open("messages.json", "r+") as f:
				a=f.read()
				print(a)
				print("hei")
				a = a if len(a) > 0 else '[]'
				temp=json.loads(a)
				temp.append({"username":self.name, "message":payload['content'], 'timestamp':time.time()})
				print(temp)
				f.seek(0)
				f.truncate()
				f.write(json.dumps(temp))
				self.history(payload)
		else:
			self.error("You're not logged in")


	

	def names(self,payload):
		with open("db.json","r") as f:
			a=f.read()
			
			self.createResponse(a,"names")
			print("hei")

					
	def history(self, payload):
		if(not self.loggedin):
			return self.error("You're not logged in")

		with open("messages.json","r+") as f:
			self.createResponse(f.read(),"history")

		
	def help(self, payload):
		# TODO - place in help.txt
		with open("help.txt","r") as f:

			helpstr=f.read()
			createResponse(helpstr,"help")

		

	def error(self, something):


		self.createResponse(something,"error")
		


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
