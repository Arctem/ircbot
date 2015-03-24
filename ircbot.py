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
            return False:
        if msg[-1] != '\n':
            msg += '\n'
        self.sock.send(msg.encode())
        return True

    def connect(self, host, port, rooms = None):
        if sock:
            return False

        self.sock=socket.socket()
        self.sock.connect((host, port))
         
        self.sendmsg("NICK {}".format(nick), "UTF-8")
        self.sendmsg("USER {} {} bla :{}".format(nick, host, realname))

        self.sendmsg("JOIN #glory");
         
        while 1:
            readbuffer = readbuffer+s.recv(1024).decode("UTF-8")
            temp = str.split(readbuffer, "\n")
            readbuffer=temp.pop()
         
            for line in temp:
                line = str.rstrip(line)
                line = str.split(line)
         
                if(line[0] == "PING"):
                    s.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
                if(line[1] == "PRIVMSG"):
                    sender = ""
                    for char in line[0]:
                        if(char == "!"):
                            break
                        if(char != ":"):
                            sender += char 
                    size = len(line)
                    i = 3
                    message = ""
                    while(i < size): 
                        message += line[i] + " "
                        i = i + 1
                    message.lstrip(":")
                    s.send(bytes("PRIVMSG %s %s \r\n" % (sender, message), "UTF-8"))
                for index, i in enumerate(line):
                    print(line[index])


def main():
    #bot = IRCBot("ircbot", "IRC Bot")
    #bot.connect("irc.arctem.com", 6667)
    sock = socket.socket()
    sock.connect(('irc.arctem.com', 6667))
    sock.send("NICK ircbot\n".encode())
    sock.send("USER ircbot irc.arctem.com bla :IRC Bot\n".encode())
    sock.send("JOIN #glory\n".encode())

    while True:
        input_ready, output_ready, except_ready = select.select([sock, sys.stdin], [], [])

        for item in input_ready:
            if item == sys.stdin:
                sock.send("{}\n".format(item.readline().strip()).encode())
            else:
                recv = item.recv(1024).decode()
                print(recv)
                if(recv.startswith("PING")):
                    reply = recv[5:]
                    sock.send("PONG {}\n".format(reply).encode())


if __name__ == '__main__':
    main()