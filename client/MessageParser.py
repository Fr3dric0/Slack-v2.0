import json
from parseexception import ParseException

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
            raise ParseException(e, 'Could not parse response')

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            raise ParseException(
                'res: {}'.format(payload['response']),
                'Strange Response'
            )


    def parse_error(self, payload):
        raise ParseException(payload['content'], 'Error from Server')


    def parse_info(self, payload):
        message = self.chat_elem({ 'username': 'server', 'message': payload['content'] })
        self.history.append(message)

        return '\n'.join(self.history)


    def parse_login(self, payload):
        return self._render_history(payload['content'])
        

    def parse_logout(self, payload):
        return payload['content']


    def parse_msg(self, payload):
        message = self.chat_elem({ 'username': payload['sender'], 'message': payload['content'] })
        self.history.append(message) # Append current chat to msg

        return '\n'.join(self.history)


    def parse_history(self, payload):
        return self._render_history(payload['content'])


    def parse_names(self, payload):
        content = payload['content']
        return self._render_names(content)


    def _render_history(self, hist):
        """ 
        Renders a list of messages, where each element is expected to be formatted as
        """
        hist = hist if len(hist) else '[]'
        history = json.loads(hist) if type(hist) is str else hist
        # Generate the chat message
        data = list(map(lambda m: self.chat_elem(m), history))

        self.history = data # Assume we can safelly replace current history

        return '\n'.join(data)


    def _render_names(self, users_str):
        if not users_str:
            return ''

        users = json.loads(users_str)

        rendered = []
        for i in range(len(users)):
            rendered.append('{:>2}. {}'.format(
                i + 1, 
                users[i]['username'] if 'username' in users[i] else '[unkown]')
            )

        # Append newline to every item
        return '\n' + '\n'.join(rendered)


    def chat_elem(self, message):
        """
        param:  dict    message     Representing a signle user message
        """
        # Catches situations where the message is just a string
        if type(message) is str:
            user = 'server'
            msg = message
        else:
            # In case the message is the default 'message' response
            if 'sender' in message:
                user = message['sender']
                msg = message['content'] if 'content' in message else '<missing message>'
            else:
                user = message['username'] if 'username' in message else '[server]'
                msg = message['message'] if 'message' in message else '<missing message>'

        return """-------------------------------
{:<10}
{:<15}
-------------------------------""".format(user, msg)

