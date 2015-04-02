import re

from ircbot.plugin import IRCPlugin

class IRCCommand(IRCPlugin):
    """A command is a type of plugin that reacts specifically to messages of
    the form '<botname>[:,] <commandname> <args>'
    """

    def __init__(self, command, function, description=None):
        IRCPlugin.__init__(self)
        self.command = command
        self.function = function
        self.description = description

        self.triggers['PRIVMSG'] = self.privmsg
        self.responses['PRIVMSG'] = self.run

    def privmsg(self, prefix, args):
        channel = args[0]
        args = ' '.join(args[1:])

        reg = re.compile('^{}[:,] {}'.format(self.owner.nick, self.command))
        return bool(reg.match(args))

    def run(self, prefix, args):
        print(prefix, args)
        user = prefix.split('!')[0]
        chan = args.pop(0)
        self.function(user, chan, args[1:])

    def name(self):
        return self.command

    def description(self):
        return self.description