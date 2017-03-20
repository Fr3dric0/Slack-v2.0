

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Logger:

    def __init__(self, filename):
        self.filename = filename if filename else None

    def message(self, opt):
        if type(opt) == dict:
            if 'title' in opt:
                print(bcolors.BOLD + str(opt['title']) + bcolors.ENDC)
            if 'message' in opt:
                print(str(opt['message']))
        else:
            print(opt)

    def error(self, opt):
        if 'title' in opt:
            print(bcolors.FAIL + bcolors.BOLD + str(opt['title']) + bcolors.ENDC)
        if 'message' in opt:
            print(bcolors.FAIL + str(opt['message']) + bcolors.ENDC)
    
    def warn(self, opt):
        if 'title' in opt:
            print(bcolors.WARNING + bcolors.BOLD + str(opt['title']) + bcolors.ENDC)
        if 'message' in opt:
            print(bcolors.WARNING + str(opt['message']) + bcolors.ENDC)