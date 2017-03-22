
class History:

    def __init__(self, filename):
        self.filename = filename

    
    def find(self):
        pass

    

    def _read_file(self):
        try:
            with open(filename, 'r+') as f:
                return f.read()
        except:
            return str([])

    
    