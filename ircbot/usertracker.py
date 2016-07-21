from ircbot.command import IRCCommand
from ircbot.events import sendmessage
from ircbot.models import User, Message
from ircbot.plugin import IRCPlugin
import ircbot.user_controller as user_controller

class UserTracker(IRCPlugin):
    def directmessage(self, source, target, msg):
        user_controller.save_message(source, target, msg)

    def generalmessage(self, source, target, msg):
        user_controller.save_message(source, target, msg)

class LastMessage(IRCCommand):
    def __init__(self):
        IRCCommand.__init__(self, 'last', self.last_cmd, args='<username>',
                            description='Shows the last activity by the given user.')

    def last_cmd(self, user, chan, args):
        last = user_controller.get_last_message(chan, args)
        if last:
            self.fire(sendmessage(chan, str(last)))
        else:
            if args:
                self.fire(sendmessage(chan, '{}: No message found for {}.'.format(user.nick, args)))
            else:
                self.fire(sendmessage(chan, '{}: No message found.'.format(user.nick)))
