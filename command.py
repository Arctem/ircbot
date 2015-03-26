import re

from plugin import IRCPlugin

class IRCCommand(IRCPlugin):
    """A command is a type of plugin that reacts specifically to messages of
    the form '<botname>[:,] <commandname> <args>'
    """

    def __init__(self, name, function):
        IRCPlugin.__init__(self)
        self.name = name
        self.function = function

    def trigger(self, prefix, args):
        channel = args[0]
        args = ' '.join(args[1:])

        reg = re.compile('^{}[:,] {}'.format(self.owner.nick, self.name))
        return bool(reg.match(args))

    def run(self, prefix, args):
        print(prefix, args)
        user = prefix.split('!')[0]
        chan = args.pop(0)
        self.function(self, user, chan, args[1:])