from circuits import Debugger

from ircbot.ircbot import IRCBot
from ircbot.command import IRCCommand
from ircbot.help import Help
from ircbot.events import sendmessage

def main():
    bot = IRCBot(host="irc.sudo-rmrf.net", port=6667, channel="#services", nick="testbot")
    Help("Intro", "Outro").register(bot)
    IRCCommand('boop', lambda user, chan, args: bot.fire(sendmessage(chan, user.nick + ': bop'))).register(bot)
    d = Debugger().register(bot)
    bot.run()

if __name__ == '__main__':
    main()
