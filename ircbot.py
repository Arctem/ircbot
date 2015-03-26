#!/usr/bin/env python3
  
import sys
import socket
import string
import select

import ircutil
 

class IRCBot:
    def __init__(self, nick, realname):
        self.nick = nick
        self.realname = realname
        self.readbuffer = ""
        self.sock = None

    def sendmsg(self, msg):
        if not msg:
            return False
        print('Sending: {}'.format(msg))
        if msg[-1] != '\n':
            msg += '\n'
        self.sock.send(msg.encode())
        return True

    def connect(self, host, port, rooms = None):
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

        inputs = [self.sock, sys.stdin]
        while True:
            in_ready, out_ready, except_ready = select.select(inputs, [], [])

            for item in in_ready:
                if item == sys.stdin:
                    self.sendmsg(item.readline().strip())
                elif item == self.sock:
                    recv = item.recv(4096).decode()
                    for recv in recv.split('\n'):
                        if recv == None:
                            print('Remote socket {} closed.'.format(self.sock))
                            break
                        if len(recv) == 0:
                            continue

                        prefix, cmd, args = ircutil.parsemsg(recv)
                        if cmd == 'PING':
                            self.sendmsg('PONG {}'.format(args[0]))
                        elif cmd == 'MODE':
                            if prefix == self.nick:
                                for room in self.rooms:
                                    self.sendmsg("JOIN {}".format(room))
                            else:
                                print('Unhandled: {}'.format(recv))
                        else:
                            print('Unrecognized command {}: {}'.format(cmd, recv))

                else:
                    print('Something broke: {}'.format(item))


def main():
    bot = IRCBot("ircbot", "IRC Bot")
    bot.connect("irc.arctem.com", 6667, ['#glory'])
    bot.process()


if __name__ == '__main__':
    main()