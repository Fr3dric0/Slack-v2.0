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

    self.possible_responses = {
            'login': self.login,
            'logout': self.logut,
            'msg':self.msg,
            'names':self.names
            'help': self.names
            'history': self.history
        # More key:values pairs are needed  
        }
    self.loggedin=False


    def handle(self):
        """
        This method handles the connection between a client and the server.
        """

        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        # Loop that listens for messages from the client
        while True:

            received_string = self.connection.recv(4096)
            payload=json.loads(received_string)

            if payload['response'] in self.possible_responses:
                return self.possible_responses[payload['response']](payload)
            else:
                return self.error()





            
            # TODO: Add handling of received payload from client
    def createResponse(username,content,response):
        message=


    def login(self, payload):
        if(self.loggedin):
            self.history(self, payload)
        else:
            if(re.match([a-zA-Z0-9],payload["content"])):
                self.name=payload["content"]
                with open(db.json as f:
                    temp={"username":self.name,"lastlogin":time.time()}
                    f.write(json.dump(temp))
                    self.history(payload)



        

    def logout(self, payload):
        if(self.loggedin):
            with open("db.json") as f:
                temp=json.loads(f.read)


                

        pass

    def msg(self, payload):
        pass

    def names(self,payload):
        pass

    def history(self, payload):
        pass

    def help(self, payload):
        pass

    def error(self, payload):
        pass


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
