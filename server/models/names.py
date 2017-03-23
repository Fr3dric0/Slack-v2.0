import json
import time

class Names:


    def __init__(self, filename):

        self.filename = filename
    
    
    def find(self):
        f = self._read_file()
        try:
            return json.loads(f) if len(f) > 1 else []
        except:
            return []


    def findOne(self, username):
        names = self.find()
        
        for name in names:
            if username == name['username']:
                return name
        
        return None


    def append(self, username):
        names = self.find()

        name = self.render_name(username)
        names.append(name)
        
        if not self._write_file(json.dumps(names)):
            raise IOError('Could not append {} to names'.format(username))

        return name

    def remove(self, username):
        pass

    def render_name(self, username):
        return {
            'username': username,
            'last_login': str(time.time())
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