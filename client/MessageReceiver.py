# -*- coding: utf-8 -*-
from threading import Thread
import json
from Logger import Logger

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """
    history = []

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """
        Thread.__init__(self)
        
        self.daemon = True
        
        self.client = client
        self.connection = connection
        

    def run(self):
        while True:
            response = self.connection.recv(4096).decode()

            if not response:
                print('LOST CONNECTION WITH SERVER')
                break

            self.client.receive_message(response)
            
        
            
