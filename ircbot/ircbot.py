#!/usr/bin/env python3

import re
import sys

from circuits import Component
from circuits.net.sockets import TCPClient, connect
from circuits.protocols.irc import IRC, PRIVMSG, USER, NICK, JOIN

from circuits.protocols.irc import ERR_NICKNAMEINUSE
from circuits.protocols.irc import RPL_ENDOFMOTD, ERR_NOMOTD

import colorama
colorama.init()
from colorama import Fore

from ircbot.events import *
from ircbot.models import User

class IRCBot(Component):
    channel = 'ircbot'

    def init(self, host="irc.sudo-rmrf.net", port="6667", channel="#csb", nick="testbot"):
        self.host = host
        self.port = int(port)
        self.nick = nick
        self.channel = channel

        # Add TCPClient and IRC to the system.
        TCPClient(channel=self.channel).register(self)
        IRC(channel=self.channel).register(self)

    #triggered when initialization is done
    def ready(self, component):
        self.fire(debugalert("Connecting!"))
        self.fire(connect(self.host, self.port))

    def connected(self, host, port):
        self.fire(NICK(self.nick))
        self.fire(USER(self.nick, self.nick, host, "I'm a test bot!"))

    def disconnected(self):
        raise SystemExit(0)

    #triggered by numeric events
    #see https://github.com/circuits/circuits/blob/master/circuits/protocols/irc/numerics.py
    def numeric(self, source, numeric, *args):
        if numeric == ERR_NICKNAMEINUSE:
            self.fire(NICK("{0:s}_".format(self.nick)))
        elif numeric in (RPL_ENDOFMOTD, ERR_NOMOTD):
            self.fire(JOIN(self.channel))

    def privmsg(self, source, target, message):
        source = User(*source)

        self.fire(debugout("{} <{}> {}".format(source.nick, target, message)))

        regex_cmd = re.compile(r'^\.(?P<command>[^\s]+)(?: (?P<args>.*))?$'.format(nick=self.nick))
        regex_direct = re.compile(r'^{nick}[:,] (?P<msg>.+)$'.format(nick=self.nick))

        if target.startswith("#"):
            cmd_match = regex_cmd.search(message)
            direct_match = regex_direct.search(message)
            if cmd_match:
                cmd = cmd_match.group('command')
                args = cmd_match.group('args')
                self.fire(command(source, target, cmd, args))
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

    def debugout(self, msg):
        print('{}{}{}'.format(Fore.YELLOW, msg, Fore.RESET))

    def debugalert(self, msg):
        print('{}{}{}'.format(Fore.RED, msg, Fore.RESET))
