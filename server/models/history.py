import time

class History:
    """
    Model for the history data. 
    Has the ability to find
    """
    def __init__(self, filename):
        self.filename = filename

    
    def find(self):
        f = self._read_file()
        try:
            return json.loads(f)
        except:
            return None


    def append(self, sender, message, response = 'message'):
        elem = self.render_mesage(sender, message, response)
        
        try:
            data = json.loads(self._read_file())
        except:
            raise IOError('[History model] Could not convert data in {} to dict'.format(self.filename))

        data.append(elem)
        self._write_file(json.dumps(data))
        return data
    

    def render_mesage(self, sender, message, response):
        return {
            'timestamp': time.time(),
            'sender': sender,
            'response': response,
            'content': message
        }

    def _read_file(self):
        try:
            with open(filename, 'r+') as f:
                return f.read()
        except:
            return str([])

    
    def _write_file(self, data):
        try:
            with open(filename, 'r+') as f:
                f.write(data)
        except:
            return False
        
        return True