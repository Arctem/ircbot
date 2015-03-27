#!/usr/bin/env python3

import os
import sys
import socket
import string
import select

from ircbot import ircutil
from ircbot.plugin import IRCPlugin
from ircbot.command import IRCCommand
 

class IRCBot:
    def __init__(self, nick, realname):
        self.nick = nick
        self.realname = realname
        self.readbuffer = ""
        self.sock = None
        self.plugins = []

    def sendmsg(self, msg):
        if not msg:
            return False
        print('Sending: {}'.format(msg))
        if msg[-1] != '\n':
            msg += '\n'
        self.sock.send(msg.encode())
        return True

    def send_privmsg(self, channel, msg):
        self.sendmsg('PRIVMSG {} {}'.format(channel, msg))

    def connect(self, host, port = 6667, rooms = None):
        if self.sock:
            return False

        self.sock=socket.socket()
        self.sock.connect((host, port))
        self.rooms = rooms or []
         
        self.sendmsg("NICK {}".format(self.nick))#, "UTF-8")
        self.sendmsg("USER {} {} bla :{}".format(self.nick, host, self.realname))

    def process(self):
        if not self.sock:
            return False

        response_functions = self.get_responses()

        inputs = [self.sock]
        if os.name != 'nt':
            inputs.append(sys.stdin)

        partial_input = ''

        while True:
            in_ready, out_ready, except_ready = select.select(inputs, [], [])

            for item in in_ready:
                if item == sys.stdin:
                    self.sendmsg(item.readline().strip())
                elif item == self.sock:
                    recv = item.recv(4096).decode()
                    recv = partial_input + recv
                    recv = recv.split('\n')
                    partial_input = recv.pop()

                    for recv in recv:
                        if recv == None:
                            print('Remote socket {} closed.'.format(self.sock))
                            break
                        if len(recv) == 0:
                            continue

                        prefix, cmd, args = ircutil.parsemsg(recv)
                        if cmd in response_functions.keys():
                            response_functions[cmd](prefix, args)
                        else:
                            print('Unrecognized command {}: {} | {}'
                                .format(cmd, prefix, args))

                else:
                    print('Something broke: {}'.format(item))

    def register(self, plugin):
        plugin.set_owner(self)
        self.plugins.append(plugin)

    def get_responses(self):
        return {
            'PING': lambda pre, args: self.sendmsg('PONG {}'.format(args[0])),
            'MODE': self.get_mode,
            'PRIVMSG': self.handle_privmsg
        }

    def get_mode(self, prefix, args):
        if prefix == self.nick:
            for room in self.rooms:
                self.sendmsg('JOIN {}'.format(room))
        else:
            print('Unhandled JOIN: {} | {}'.format(prefix, args))

    def handle_privmsg(self, prefix, args):
        for plugin in self.plugins:
            if plugin.trigger(prefix, args):
                plugin.run(prefix, args)
