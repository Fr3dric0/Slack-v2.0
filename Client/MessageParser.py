import json

class MessageParser():
    legal_methods = ['login <username>', 'logout', 'msg <message>', 'history', 'names', 'help']

    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'login': self.parse_login,
            'logout': self.parse_logout,
            'msg': self.parse_msg,
            'history': self.parse_history
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

    def parse_login(self, payload):
        pass
    
    def parse_logout(self, payload):
        pass
    
    def parse_msg(self, payload):
        pass
    
    def parse_history(self, payload):
        pass
    # Include more methods for handling the different responses... 
