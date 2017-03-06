import json

class MessageParser():
    legal_methods = ['login <username>', 'logout', 'msg <message>', 'history', 'names', 'help']

    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info
	    # More key:values pairs are needed	
        }

    def parse(self, payload):
        payload = json.loads(payload)

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            print("YALLAYALLA")
            # Response not valid

    def parse_error(self, payload):
        print("HEI")
    def parse_info(self, payload):
        print("YO")
    # Include more methods for handling the different responses... 
