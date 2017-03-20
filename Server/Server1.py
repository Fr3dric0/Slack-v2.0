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

            if payload['request'] in self.possible_responses:
                return self.possible_responses[payload['request']](payload)
            else:
                return self.error(payload)


    def createResponse(self, content,response):
        message=json.dumps({"timestamp":time.time(), "sender":self.name, "response":response, "content":content})
        self.connection.sendall(message.encode())

    def login(self, payload):
        if(self.loggedin):
            self.history(self, payload)
        else:
            if(re.match("^[A-Za-z0-9_-]*$",payload["content"])):
                self.name=payload["content"]

                with open("db.json","w+") as f:
                    print(f.read())
                    fp=json.loads(f.read())

                    temp={"username":payload['content'],"lastlogin":time.time()}
                    self.name=payload['content']
                    fp.append(temp)
                    print(fp)
                    print(json.dumps(fp))
                    f.write(json.dumps(fp))
                    self.history(payload)

        

    def logout(self, payload):
        if(self.loggedin):
            with open("db.json") as f:
                temp=json.loads(f.read())
                try:
                    i=list(filter(lambda p: p["username"]==self.name,temp))[0]
                    temp.remove(i)
                    f.write(json.dumps(temp))
                    self.loggedin=False
                except:
                    print("username does not exist")
        else:
            self.error(payload)


    def msg(self, payload):
        if(self.loggedin):
            with open("messages.json") as f:
                temp=json.load(f)
                temp.append({"username":self.name, "message":payload['content'], 'timestamp':time.time()})
                f.write(json.dumps(temp))
                self.history()
        else:
            self.error(payload)


    

    def names(self,payload):
        with open("db.json") as f:
            temp=f.read()
            self.createResponse(temp,"names")

                
            

    
    def history(self, payload):
        with open("messages.json") as f:
            self.createResponse(f.read(),"messages")

        

    def help(self, payload):
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


        createResponse("Something went wrong","error")
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
