import irclib
import random
import time
import thread
import sys

class IRCBot:
    message_buffer = []
    sleep_time = .5 #Minimum time between messages.
    default_timeout = 0.2
    
    def __init__(self, network = 'irc.cs.nmt.edu', port = 6667,
        channel = ('#bottest', ), nick = 'testbot', name = 'None', debug = False):
        #Debug data
        irclib.DEBUG = debug
        
        #Connection data.
        self.network = network
        self.port = port
        self.channel = channel
        self.nick = nick
        self.name = name
        self.ipv6 = False
    
    #Initialize the irc object and initialize the handlers.
    def initIRC(self):
        #Create an IRC object.
        self.irc = irclib.IRC()

        # Register handlers
        self.irc.add_global_handler('privnotice', self.handle_priv_notice) #Private notice
        self.irc.add_global_handler('welcome', self.handle_echo) #Welcome message
        self.irc.add_global_handler('yourhost', self.handle_echo) #Host message
        self.irc.add_global_handler('created', self.handle_echo) #Server creation message
        self.irc.add_global_handler('myinfo', self.handle_echo) #"My info" message
        self.irc.add_global_handler('featurelist', self.handle_echo) #Server feature list
        self.irc.add_global_handler('luserclient', self.handle_echo) #User count
        self.irc.add_global_handler('luserop', self.handle_echo) #Operator count
        self.irc.add_global_handler('luserchannels', self.handle_echo) #Channel count
        self.irc.add_global_handler('luserme', self.handle_echo) #Server client count
        self.irc.add_global_handler('n_local', self.handle_echo) #Server client count/maximum
        self.irc.add_global_handler('n_global', self.handle_echo) #Network client count/maximum
        self.irc.add_global_handler('luserconns', self.handle_echo) #Record client count
        self.irc.add_global_handler('luserunknown', self.handle_echo) #Unknown connections
        self.irc.add_global_handler('motdstart', self.handle_echo) #Message of the day ( start)
        self.irc.add_global_handler('motd', self.handle_echo_no_space) #Message of the day
        self.irc.add_global_handler('edofmotd', self.handle_echo) #Message of the day ( end)
        self.irc.add_global_handler('join', self.handle_join) #Channel join
        self.irc.add_global_handler('namreply', self.handle_echo_no_space) #Channel name list
        self.irc.add_global_handler('endofnames', self.handle_echo_no_space) #Channel name list ( end)
        self.irc.add_global_handler('invite', self.handle_invite) #Invitation to a new channel.
        self.irc.add_global_handler('privmsg', self.handle_priv_message)
        self.irc.add_global_handler('pubmsg', self.handle_pub_message)
    
    #Connect and begin processing.
    def start(self):
        #Create a server object, connect and join the channel.
        self.server = self.irc.server()
        self.server.connect(self.network, self.port, self.nick, ircname = self.name, ipv6 = self.ipv6)
        for s in self.channel:
            self.server.join(s)

        #Send test messages.
        thread.start_new_thread(self.process_message_buffer, ())

        #Start infinite loop.
        while True:
            self.process(self.default_timeout)
        #self.irc.process_forever()
    
    #Carries out one iteration of IRC communications.
    def process(self, timeout = 0.2):
        self.nick = self.server.get_nickname()
        self.irc.process_once(timeout)
    
    #Avoids server flooding.
    def process_message_buffer(self):
        try:
            while True:
                if len(self.message_buffer) > 2:
                    print ' Message buffer: {}'.format(len(self.message_buffer))
                if len(self.message_buffer) > 0:
                    msg = self.message_buffer.pop(0)
                    if msg[1]:
                        msg[2].action(msg[3].target(), msg[0])
                    else:
                        msg[2].privmsg(msg[3].target(), msg[0])
                    time.sleep(self.sleep_time)
                else:
                    time.sleep(0.1)
        except:
            print sys.exc_info()
    
    #Add things to message buffer.
    def add_to_buffer(self, connection, event, output, is_action = False):
        self.message_buffer.append((is_action, connection, event, output))
    
    #Generic echo handler
    #Output initial information from server, with leading space.
    def handle_echo(self, connection, event):
        print
        print ' '.join(event.arguments())

    #Generic echo handler
    #Output initial information from server, but without leading space.
    def handle_echo_no_space(self, connection, event):
        print ' '.join(event.arguments())

    #Handle private notices
    def handle_priv_notice(self, connection, event):
        if event.source():
            print ':: ' + event.source() + ' ->' + event.arguments()[0]
        else:
            print event.arguments()[0]

    #Handle someone joining a channel.
    def handle_join(self, connection, event):
        #Sources needs to be split into just the name.
        #Data comes in the format nickname!user@host
        print event.source().split('!')[0] + ' has joined ' + event.target()

    #Accept invitations into new channels.
    def handle_invite(self, connection, event):
        connection.join(event.arguments()[0])

    #Handle private messages.
    def handle_priv_message(self, connection, event):
        print event.source().split('!')[0] + ': ' + event.arguments()[0]

    #Handle public messages.
    def handle_pub_message(self, connection, event):
        print event.target() + '> ' + event.source().split('!')[0] + ': ' + event.arguments()[0]
