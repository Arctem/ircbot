from circuits import Debugger

from ircbot.ircbot import IRCBot
from ircbot.command import IRCCommand
from ircbot.help import Help
from ircbot.events import sendmessage
from ircbot.usertracker import UserTracker, LastMessage

from ircbot import storage
# storage.initialize('sqlite:///testbot.db')
storage.initialize()

def main():
    bot = IRCBot(host="irc.sudo-rmrf.net", port=6667, channel="#bot", nick="testbot")
    h = Help("Intro", "Outro").register(bot)
    UserTracker().register(bot)
    LastMessage().register(bot)
    IRCCommand('boop', lambda user, chan, args: bot.fire(sendmessage(chan, user.nick + ': bop'))).register(bot)
    d = Debugger().register(bot)
    bot.run()

if __name__ == '__main__':
    main()
