import re

from ircbot.plugin import IRCPlugin
from ircbot.events import enablehelp, debugout

class IRCCommand(IRCPlugin):
    """A command is a type of plugin that reacts specifically to messages of
    the form '<botname>[:,] <commandname> <args>'
    """

    def __init__(self, name, function, description=None):
        super(IRCCommand, self).__init__()
        self._name = name
        self._function = function
        self._description = description

    def ready(self, component):
        self.fire(debugout("Loaded {} command".format(self._name)))
        self.fire(enablehelp(self))

    def command(self, source, target, cmd, args):
        if cmd == self._name:
            self._function(source, target, args)

    def name(self):
        return self._name

    def description(self):
        return self._description
