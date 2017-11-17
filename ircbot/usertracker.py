from ircbot.command import IRCCommand
from ircbot.events import reply
from ircbot.models import User, Message
from ircbot.plugin import IRCPlugin
import ircbot.user_controller as user_controller


class UserTracker(IRCPlugin):

    def join(self, info, channel):
        nick, realname, address = info
        user = user_controller.get_or_create_user(nick, name=realname)
        return user_controller.add_user_to_channel(user, channel)

    def quit(self, info, channel):
        nick, realname, address = info
        user = user_controller.get_or_create_user(nick, name=realname)
        return user_controller.remove_user_from_channel(user, channel)


class LastMessage(IRCCommand):

    def __init__(self):
        IRCCommand.__init__(self, 'last', self.last_cmd, args='<username>',
                            description='Shows the last activity by the given user.')

    def last_cmd(self, ctx):
        speaker = None
        if ctx.command_args:
            speaker = user_controller.get_user(ctx.command_args)
            if not speaker:
                self.fire(reply(ctx, '{user}: Could not find user {}.', target=speaker))
                return
        last = user_controller.get_last_message(ctx.channel, speaker)
        if last:
            self.fire(reply(ctx, str(last)))
        else:
            if speaker:
                self.fire(reply(ctx, '{user}: No message found for {target}.', target=speaker))
            else:
                self.fire(reply(ctx, '{user}: No message found.'))
