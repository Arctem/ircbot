from ircbot.command import IRCCommand
from ircbot.events import sendmessage

class Help(IRCCommand):
    def __init__(self, intro=None, outro=None):
        IRCCommand.__init__(self, 'help', self.help_cmd)
        self.intro = intro
        self.outro = outro
        self.modules = []

    def help_cmd(self, user, chan, args):
        response = []

        if self.intro:
            response.append(self.intro)

        commands = sorted(map(lambda c: c.name(), self.modules))
        commands = ', '.join(commands)
        if commands:
            response.append('Commands: {}.'.format(commands))

        if self.outro:
            response.append(self.outro)

        response = ' '.join(response)

        self.fire(sendmessage(chan, response))

    def enablehelp(self, module):
        self.modules.append(module)
