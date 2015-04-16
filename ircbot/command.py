import re

from ircbot.plugin import IRCPlugin

class IRCCommand(IRCPlugin):
    """A command is a type of plugin that reacts specifically to messages of
    the form '<botname>[:,] <commandname> <args>'
    """

    def __init__(self, command, function, description=None, blocks=True,
            priority=10):
        IRCPlugin.__init__(self)
        self.command = command
        self.function = function
        self.description = description
        self.blocks = blocks

        self.triggers['PRIVMSG'] = (priority, self.privmsg)

    def privmsg(self, prefix, args):
        channel = args.pop(0)
        user = prefix.split('!')[0]

        reg = re.compile(r'^{}[:,] {}'.format(self.owner.nick, self.command))
        trig = bool(reg.match(' '.join(args)))

        if trig:
            args = args[0].split(None, 3)
            args = args[2] if len(args) == 3 else None
            self.function(user, channel, args)

        if trig and self.blocks:
            return 2
        else:
            return trig

    def name(self):
        return self.command

    def description(self):
        return self.description
