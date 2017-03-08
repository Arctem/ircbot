import re

from ircbot.plugin import IRCPlugin
from ircbot.events import enablehelp, enablestats, debugout

def make_cmd_description(cmd, args, description=None):
    cmd = cmd.strip()
    if args:
        cmd = cmd + ' ' + args.strip()
    if not description:
        description = 'No further description available.'
    return 'Run with .{}. {}'.format(cmd, description)

class IRCCommand(IRCPlugin):
    """A command is a type of plugin that reacts specifically to messages of
    the form '.<commandname> <args>'
    """

    def __init__(self, name, function, args=None, description=None):
        super(IRCCommand, self).__init__()
        self._name = name
        self._function = function
        self._description = make_cmd_description(name, args, description)

    def ready(self, component):
        self.fire(debugout("Loaded {} command".format(self._name)))
        self.fire(enablehelp(self))
        self.fire(enablestats(self))

    def command(self, source, target, cmd, args):
        if cmd == self._name:
            self._function(source, target, args)

    def name(self):
        return self._name

    def description(self):
        return self._description

    def stats(self):
        return set()