import json

class MessageParser():
    # Store the current chat history with the clients session
    history = []

    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'logout': self.parse_logout,
            'message': self.parse_msg,
            'history': self.parse_history,
            'names': self.parse_names
        }

    def parse(self, data):
        try:
            payload = json.loads(data)
        except Exception as e:
            return {
                'title': 'Nothing in response', 
                'message': e
            }

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            print(payload['response'])


    def parse_error(self, payload):
        return payload['content']


    def parse_info(self, payload):
        return payload['content']


    def parse_login(self, payload):
        return self._render_history(payload['content'])
    

    def parse_logout(self, payload):
        return payload['content']


    def parse_msg(self, payload):
        message = { 'username': payload['sender'], 'message': payload['content']}

        msg = self.chat_elem(message)
        self.history.append(msg) # Append current chat to msg
        return msg


    def parse_history(self, payload):
        print(payload)
        return self._render_history(payload['content'])


    def parse_names(self, payload):
        content = payload['content']
        print(content)
        return ''


    def _render_history(self, hist):
        hist = hist if len(hist) else '[]'
        history = json.loads(hist) if type(hist) is str else hist
        
        # Generate the chat message
        data = list(map(lambda m: self.chat_elem(m), history))

        self.history = data # Assume we can safelly replace current history

        return '\n'.join(data)


    def chat_elem(self, message):
        """
        param:  dict    message     Representing a signle user message
        """
        user = message['username'] if 'username' in message else '[server]'
        msg = message['message'] if 'message' in message else '<missing message>'
        return """
-------------------------------
{:<10}
{:<15}
-------------------------------""".format(user, msg)

