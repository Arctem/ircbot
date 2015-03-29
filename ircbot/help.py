from ircbot.command import IRCCommand

class Help(IRCCommand):
    def __init__(self, intro=None, outro=None):
        IRCCommand.__init__(self, 'help', Help.help_cmd)
        self.intro = intro
        self.outro = outro

    def help_cmd(self, user, chan, args):
        response = []

        if self.intro:
            response.append(self.intro)

        commands = filter(lambda p: isinstance(p, IRCCommand),
            self.owner.plugins)
        commands = sorted(map(lambda c: c.name(), commands))
        commands = ', '.join(commands)
        if commands:
            response.append('Commands: {}.'.format(commands))



        if self.outro:
            response.append(self.outro)

        response = ' '.join(response)

        self.owner.send_privmsg(chan, response)
        