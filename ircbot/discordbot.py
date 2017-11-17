#!/usr/bin/env python3

import asyncio
import copy
import discord
import math
import re
import threading

from colorama import Fore

from ircbot.bot import Bot
from ircbot.context import Context
from ircbot.events import *
from ircbot.models import User, Message
import ircbot.user_controller as user_controller
import ircbot.storage as db


class DiscordContext(Context):

    def __init__(self):
        super(DiscordContext, self).__init__()
        self.app = 'discord'


@db.atomic
def get_server(orig, s=None):
    server = user_controller.get_or_create_server(orig.id, 'discord', s=s)
    server.name = orig.name
    return server


@db.atomic
def get_user(orig, server, s=None):
    user = user_controller.get_or_create_user(orig.id, server, s=s)
    user.bot = orig.bot
    user.name = orig.name
    return user


@db.atomic
def get_channel(orig, server, s=None):
    channel = user_controller.get_or_create_channel(orig.id, server, s=s)
    channel.name = orig.name
    return channel


@db.atomic
def create_message(orig, channel, user, s=None):
    message = user_controller.create_message(user, channel, orig.content, channel.private, remote_id=orig.id, s=s)
    return message


@db.atomic
def create_context_from_message(message, s=None):
    ctx = DiscordContext()
    ctx.server = get_server(message.server, s=s)
    ctx.user = get_user(message.author, ctx.server, s=s)
    ctx.channel = get_channel(message.channel, ctx.server, s=s)
    ctx.message = create_message(message, ctx.channel, ctx.user, s=s)

    return ctx


class DiscordBot(Bot):

    def __init__(self, token):
        super(DiscordBot, self).__init__()
        self.client = discord.Client()
        self.token = token
        self.init_discord_hooks()

        self.queue = asyncio.Queue()
        self.client.loop.create_task(self.background_task())

        self.fire(debugalert("DiscordBot Initialized!"))

    async def background_task(self):
        await self.client.wait_until_ready()
        while not self.client.is_closed:
            item = await self.queue.get()
            print("Got from queue: {}".format(item))
            await item

    def init_discord_hooks(self):
        client = self.client

        @client.event
        async def on_ready():
            print('Logged in as')
            print(client.user.name)
            print(client.user.id)
            print('------')

        @client.event
        async def on_message(message):
            if message.author == self.client.user:
                return

            ctx = create_context_from_message(message)

            self.fire(debugout("{} <{}:{}> {}".format(
                ctx.user.name, ctx.server.name,
                ctx.channel.name, ctx.message.message)))

            regex_cmd = re.compile(r'^\.(?P<command>[^\s]+)(?: (?P<args>.*))?$')
            cmd_match = regex_cmd.search(ctx.message.message)

            if ctx.channel.private:
                pass
            else:
                self.fire(debugout("cmd_match: {}".format(cmd_match)))
                if cmd_match:
                    ctx.command = cmd_match.group('command')
                    ctx.command_args = cmd_match.group('args')
                    self.fire(debugout("Created context: {}".format(ctx)))
                    self.fire(command(ctx))
                else:
                    self.fire(generalmessage(ctx))

    def started(self, component):
        self.fire(debugalert("Connecting!"))

        def client_loop(client, token):
            client.run(token)
        t = threading.Thread(target=client_loop, args=(self.client, self.token))
        t.start()

    def reply(self, ctx, message, **kwargs):
        self.fire(debugout('{}Sending {}: {}{}'.format(Fore.RED, ctx.channel, message, Fore.RESET)))
        async def hi():
            print("Hello")
        self.queue.put_nowait(hi())
        self.queue.put_nowait(self.client.send_message(discord.Object(ctx.channel.remote_id),
                                                       message.format(user=ctx.user.name, **kwargs)))
        print("Done putting in queue: {}".format(self.queue))
        print("Status: {}".format(self.client.loop))
