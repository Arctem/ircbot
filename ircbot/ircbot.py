#!/usr/bin/env python3

import re
import sys

from circuits import Component
from circuits.net.sockets import TCPClient, connect
from circuits.protocols.irc import IRC, PRIVMSG, USER, NICK, JOIN, NAMES

from circuits.protocols.irc import ERR_NICKNAMEINUSE
from circuits.protocols.irc import RPL_ENDOFMOTD, ERR_NOMOTD, RPL_NAMEREPLY

import colorama
colorama.init()
from colorama import Fore

from ircbot.events import *
from ircbot.models import User
import ircbot.user_controller as user_controller

class IRCBot(Component):
    channel = 'ircbot'

    def __init__(self, host="irc.sudo-rmrf.net", port="6667", channel="#csb", nick="testbot", realname='IRC Bot'):
        super(IRCBot, self).__init__()
        self.host = host
        self.port = int(port)
        self.nick = nick
        self.channel = channel
        self.realname = realname

        # Add TCPClient and IRC to the system.
        TCPClient(channel=self.channel).register(self)
        IRC(channel=self.channel).register(self)
        self.fire(debugalert("Initialized!"))

    #triggered when initialization is done
    def ready(self, component):
        self.fire(debugalert("Connecting!"))
        self.fire(connect(self.host, self.port))

    def connected(self, host, port):
        self.fire(NICK(self.nick))
        self.fire(USER(self.nick, self.nick, host, self.realname))

    def disconnected(self):
        raise SystemExit(0)

    #triggered by numeric events
    #see https://github.com/circuits/circuits/blob/master/circuits/protocols/irc/numerics.py
    def numeric(self, source, numeric, *args):
        if numeric == ERR_NICKNAMEINUSE:
            self.fire(NICK("{0:s}_".format(self.nick)))
        elif numeric in (RPL_ENDOFMOTD, ERR_NOMOTD):
            self.fire(JOIN(self.channel))

    def join(self, bot_info, channel):
        self.nick = bot_info[0]
        self.realname = bot_info[1]

    def privmsg(self, source, target, message):
        source = user_controller.get_or_create_user(*source)

        self.fire(debugout("{} <{}> {}".format(source.nick, target, message)))

        regex_action = re.compile('\x01ACTION (?P<action>.*)\x01')
        regex_cmd = re.compile(r'^\.(?P<command>[^\s]+)(?: (?P<args>.*))?$')
        regex_direct = re.compile(r'^{nick}[:,] (?P<msg>.+)$'.format(nick=self.nick))

        if target.startswith("#"):
            action_match = regex_action.search(message)
            cmd_match = regex_cmd.search(message)
            direct_match = regex_direct.search(message)
            if action_match:
                action = action_match.group('action')
                self.fire(actionmessage(source, target, action))
            elif cmd_match:
                cmd = cmd_match.group('command')
                args = cmd_match.group('args')
                self.fire(command(source, target, cmd, args or ''))
            elif direct_match:
                msg = direct_match.group('msg')
                self.fire(directmessage(source, target, msg))
            else:
                self.fire(generalmessage(source, target, message))
        else:
            pass
            #private message
            #self.fire(PRIVMSG(source[0], message))

    def sendmessage(self, target, message):
        print('{}Sending {}: {}{}'.format(Fore.RED, target, message, Fore.RESET))
        self.fire(PRIVMSG(target, message))

    def sendaction(self, target, action):
        print('{}Sending {} {}{}'.format(Fore.RED, target, action, Fore.RESET))
        self.fire(PRIVMSG(target, '\x01ACTION {}\x01'.format(action)))

    def debugout(self, msg):
        print('{}{}{}'.format(Fore.YELLOW, msg, Fore.RESET))

    def debugalert(self, msg):
        print('{}{}{}'.format(Fore.RED, msg, Fore.RESET))
