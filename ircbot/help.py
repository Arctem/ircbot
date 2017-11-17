from ircbot.command import IRCCommand
from ircbot.events import sendmessage

class Help(IRCCommand):
    def __init__(self, intro=None, outro=None):
        IRCCommand.__init__(self, 'help', self.help_cmd, args='<module> [<subcommands>]',
                            description='Show detailed information on active modules. For modules that have subtopics, add extra arguments for each one.')
        self.intro = intro
        self.outro = outro
        self.modules = []

    def help_cmd(self, ctx, user, chan, args):
        if args:
            msg = self.specific_help_message(ctx, user, chan, args)
        else:
            msg = self.general_help_message(ctx, user, chan)
        self.fire(reply(ctx, msg))

    def general_help_message(self, ctx, user, chan):
        response = []

        if self.intro:
            response.append(self.intro)

        commands = sorted(map(lambda c: c.name(), self.modules))
        commands = ', '.join(commands)
        if commands:
            response.append('Modules: {}.'.format(commands))

        if self.outro:
            response.append(self.outro)

        return ' '.join(response)

    def specific_help_message(self, ctx, user, chan, args):
        module_name = args.split()[0]
        subtopics = args.split()[1:]
        for module in self.modules:
            if module.name() == module_name:
                try:
                    if len(subtopics) > 0:
                        subhelp = module.help_topics
                        while len(subtopics) > 0:
                            subhelp = subhelp[subtopics[0]]
                            subtopics.pop(0)
                        return subhelp[None]
                except (KeyError, AttributeError):
                    return 'Could not find subtopic {} in module {}.'.format(subtopics[0], module.name())

                if module.description():
                    return module.description()
                else:
                    return 'No help message available for {}.'.format(module.name())
        return 'Could not find module {}.'.format(module_name)

    def enablehelp(self, module):
        self.modules.append(module)

    def stats(self):
        return {
            (lambda: 'There are {} modules with help info.'.format(len(self.modules)), ('help', 'count')),
        }