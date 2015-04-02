from colorama import Fore

from ircbot.plugin import IRCPlugin

class UserTracker(IRCPlugin):
    def __init__(self):
        IRCPlugin.__init__(self)

        self.rooms = {}

        self.triggers['JOIN'] = self.join_trigger
        self.responses['JOIN'] = self.join

        self.triggers['353'] = self.names_trigger
        self.responses['353'] = self.names

    def join_trigger(self, prefix, args):
        return prefix.split('!')[0] == self.owner.nick

    def join(self, prefix, args):
        room = args[0]

        if room not in self.rooms:
            self.rooms[room] = []

        self.owner.sendmsg('NAMES ' + room)

    def names_trigger(self, prefix, args):
        return args[1] == '@'

    def names(self, prefix, args):
        me = args[0]
        room = args[2]
        users = args[3].split()
        users = map(lambda u: u.strip('+&@~'), users) #probably needs more added

        new_user_list = []

        #This is done to maintain the list order
        for u in self.rooms[room]:
            if u in users:
                new_user_list.append(u)

        for u in users:
            if u not in new_user_list:
                new_user_list.append(u)

        self.rooms[room] = new_user_list
        print('{}{}: {}{}'.format(Fore.YELLOW, room, self.rooms[room],
            Fore.RESET))