#!/usr/bin/env python3

from aws_cdk import core

from bit_playlist_bot.bot_stack import BitPlaylistBotStack


app = core.App()
BitPlaylistBotStack(app, "bit-playlist-bot")

app.synth()
