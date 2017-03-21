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
            'history': self.parse_history,
            'names': self.parse_names
	    # More key:values pairs are needed	
        }

    def parse(self, payload):
        try:
            payload = json.loads(payload)
        except:
            return {
                'title': 'Nothing in response', 
                'message': payload
            }

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            print(payload['response'])
            # Response not valid

    def parse_error(self, payload):
        return payload['content']

    def parse_info(self, payload):
        return payload['content']

    def parse_login(self, payload):
        return self._render_history(payload['content'])
    
    def parse_logout(self, payload):
        return payload['content']


    def parse_msg(self, payload):
        return payload['content']


    def parse_history(self, payload):
        return payload['content']


    def parse_names(self, payload):
        content = payload['content']
        return content


    def _render_history(self, hist):
        if hist is str:
            hist = json.loads(hist)
        
        data = []
        for msg in hist:
            #user = msg['user'] if 'user' in msg else 'server'
            data.append(self.chat_elem(msg))
        
        return ''.join(data)


    def chat_elem(self, item):
        print(item)
        return """
        -------------------------------
        {:>10}
        {:<15}
        "-------------------------------"
        """.format(item)

