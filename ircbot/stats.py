import random

from ircbot.command import IRCCommand
from ircbot.events import sendmessage

class Stats(IRCCommand):
    def __init__(self):
        IRCCommand.__init__(self, 'stats', self.stats_cmd, args='[<keyword>]*',
                            description='Show various stats from active modules. Will show a random stat that fits with the keywords given.')
        self.modules = []

    def stats_cmd(self, user, chan, args):
        func, labels = self.stat(args)
        if not func:
            self.fire(sendmessage(chan, '{}: No stats found for given labels.'.format(user.nick)))
        else:
            self.fire(sendmessage(chan, '{}: {}'.format('/'.join(labels), func())))

    def stat(self, args):
        topics = set(args.split())
        stats = list(filter(lambda s: topics <= set(s[1]), self.generate_stats_set()))
        if len(stats) == 0:
            return None, None
        return random.choice(stats)

    def generate_stats_dict(self):
        stats = {}
        for m in self.modules:
            for func, labels in m.stats():
                for cat in labels:
                    if cat not in stats:
                        stats[cat] = set()
                    stats[cat].add(func)
        return stats

    def generate_stats_set(self):
        stats = set()
        for m in self.modules:
            stats |= m.stats()
        return stats

    def enablestats(self, module):
        self.modules.append(module)

    def stats(self):
        return {
            (self._cat_count, ('stats', 'types')),
            (self._stat_count, ('stats', 'types')),
        }

    def _cat_count(self):
        return 'There are {} stats categories.'.format(len(self.generate_stats_dict().keys()))
    def _stat_count(self):
        return 'There are {} available stats.'.format(len(self.generate_stats_set()))
