import re

from ircbot.command import IRCCommand
from ircbot.events import sendmessage
from ircbot.models import User, Message
import ircbot.user_controller as user_controller

cmd_regex = re.compile(r'^(?P<nick>\S+)\s+(?P<attribute>\S+)(?:\s+(?P<value>\S+))?$')

class Admin(IRCCommand):
    def __init__(self):
        super(Admin, self).__init__('admin', self.admin_cmd,
            args='<username> <option> <value>',
            description='Allows specifying certain options about users.')

    def admin_cmd(self, ctx, user, channel, args):
        if not user.admin:
            self.fire(reply(ctx, '{user}: You are not an admin.'))
            return False

        cmd_args = cmd_regex.match(args)

        if not cmd_args:
            self.fire(reply(ctx, '{user}: Could not parse command.'))
            return False

        nick = cmd_args.group('nick')
        attribute = cmd_args.group('attribute')
        value = cmd_args.group('value')

        if user_controller.set_attribute(nick, attribute, value):
            self.fire(reply(ctx, '{}: Attribute set successfully.'))
            return True
        else:
            self.fire(reply(ctx, '{}: Attribute not set.'))
            return False
