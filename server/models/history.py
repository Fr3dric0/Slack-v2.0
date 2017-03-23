import time
import json
import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class History:
    """
    Model for the history data. 
    Has the ability to find
    """
    # Copied from bccolors
    rand_colors = ['\033[94m', '\033[92m', '\033[93m', '\033[91m']

    def __init__(self, filename):
        self.filename = filename

    
    def find(self):
        f = self._read_file()
        try:
            return json.loads(f) if len(f) > 1 else []
        except:
            return []


    def append(self, sender, message, response = 'message'):
        elem = self.render_message(sender, message, response)

        try:
            data = json.loads(self._read_file())
        except:
            raise IOError('[History model] Could not convert data in {} to dict'.format(self.filename))

        data.append(elem)
        self._write_file(json.dumps(data))
        return elem
    

    def render_message(self, sender, message, response):
        return {
            'timestamp': time.time(),
            'sender': self._generate_rainbow(sender),
            'response': response,
            'content': message
        }


    def _read_file(self):
        try:
            with open(self.filename, 'r+') as f:
                return f.read()
        except:
            return str([])

    
    def _write_file(self, data):
        try:
            with open(self.filename, 'w') as f:
                f.write(data)
        except:
            return False
        
        return True

    def _generate_rainbow(self, msg):
        if not msg:
            return ''
        
        if msg.lower() == 'server':
            return bcolors.BOLD + msg + bcolors.ENDC

        return '{}{}{}'.format(random.choice(rand_colors), msg, bcolors.ENDC) 
