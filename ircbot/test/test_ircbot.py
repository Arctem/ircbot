from ircbot.ircbot import IRCBot

def main():
    bot = IRCBot("ircbot", "IRC Bot")
    bot.register(IRCCommand('boop', lambda self, user, chan, args: self.owner.send_privmsg(chan, user + ': bop')))
    bot.connect('irc.arctem.com', 6667, ['#glory'])
    #bot.connect("byrn.sudo-rmrf.net", 6667, ['#csb'])
    bot.process()


if __name__ == '__main__':
    main()