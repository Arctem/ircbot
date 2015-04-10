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

    def privmsg(self, prefix, args):
        channel = args.pop(0)
        user = prefix.split('!')[0]

        reg = re.compile(r'^{}[:,] {}'.format(self.owner.nick, self.command))
        trig = bool(reg.match(' '.join(args)))

        if trig:
            self.function(user, channel, args[1:])

        return trig

    def name(self):
        return self.command

    def description(self):
        return self.description
