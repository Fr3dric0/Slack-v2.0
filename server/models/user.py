
class User:
    """
    Inits our user-model with the basic (need-to-know) information,
    such as username `user` and the `messages` list, containing the 
    messages sent by the user.

    @param  string  user    The users username
    """
    def __init__(self, user):
        self.user = user
        self.messsages = [] # List<Message>

    def msg(self, msg):
        self.messages.append(msg)
        return msg
		
