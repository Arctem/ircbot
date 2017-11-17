from circuits import Component

import colorama
colorama.init()
from colorama import Fore

class Bot(Component):

    def __init__(self):
        super(Bot, self).__init__()

    def debugout(self, msg):
        print('{}{}{}'.format(Fore.YELLOW, msg, Fore.RESET))

    def debugalert(self, msg):
        print('{}{}{}'.format(Fore.RED, msg, Fore.RESET))
