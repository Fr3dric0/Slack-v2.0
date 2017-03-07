import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

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

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # TODO: Finish init process with necessary code
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

        while True:
            print('--- Choose action ---')
            print('\t' + '\n\t'.join(self.legal_methods))
            action = input('> ')
            method = None
            payload = None

            if action == 'login':
                payload = input('username: ')
                method = self.login
            elif action == 'logout':
                method = self.logout
            elif action == 'names':
                method = self.names
            elif action == 'history':
                method = self.history
            elif action == 'msg':
                payload = input('message: ')
                method = self.message
            elif action == 'help':
                method = self.help
            else:
                print('Illegal action! ({})'.format(action))
                continue


            try:
                send_payload(method(payload) if payload else method())
            except Exception as e:
                pass

        #self.connection.sendall(json.dumps({"message": 'hei'}).encode())
        #recieved = self.connection.recv(1024).decode()
        #print(recieved)


    def disconnect(self):
        # TODO: Handle disconnection
        pass

    def receive_message(self, message):
        # TODO: Handle incoming message
        pass

    def send_payload(self, data):
        # TODO: Handle sending of a payload
        pass
        
    # More methods may be needed!
    def login(self, username):
        print(username)
        pass

    def logout(self):
        pass

    def names(self):
        pass

    def history(self):
        pass

    def msg(self, message):
        pass

    def help(self):
        pass


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
