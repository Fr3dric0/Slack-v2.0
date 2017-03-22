# -*- coding: utf-8 -*-
from threading import Thread
import json
import sys
from Logger import Logger

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """
        Thread.__init__(self)
        # Flag to run thread as a deamon
        self.daemon = True
        
        self.client = client
        self.connection = connection
        

    def run(self):
        while True:
            response = self.connection.recv(8192).decode()

            if not response:
                Logger(None).error('LOST CONNECTION WITH SERVER')
                self.client.receive_message('DIE') # Tell the client to stop

            self.client.receive_message(response)
            
        
            
