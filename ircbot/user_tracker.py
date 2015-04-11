from colorama import Fore

from ircbot.plugin import IRCPlugin

class UserTracker(IRCPlugin):
    def __init__(self):
        IRCPlugin.__init__(self)

        self.rooms = {}

        self.triggers['JOIN'] = self.join
        #should also track MODE for other users

        self.triggers['353'] = self.names

    def join(self, prefix, args):
        user = prefix.split('!')[0]
        chan = args.pop(0)

        trig = user == self.owner.nick

        if trig:

            if chan not in self.rooms:
                self.rooms[chan] = []

            self.owner.sendmsg('NAMES ' + chan)
        else:
            self.rooms[chan].append(user)

        return trig

    def part(self, prefix, args):
        user = prefix.split('!')[0]
        chan = args.pop(0)

        self.rooms[chan].remove(user)


    def names(self, prefix, args):
        trig = args[1] == '@'

        if trig:
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

        return trig
