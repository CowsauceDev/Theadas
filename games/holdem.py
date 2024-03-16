# Theadas Bot is a Discord bot allowing users to play various games with each other.
# Copyright © 2024  Jester (@cowsauce)

# This file is part of Theadas Bot.

# Theadas Bot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Theadas Bot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import config
from theadas import User

import discord

import random
from enum import Enum

name = "Texas Hold 'Em"

description = '''
    This game is not yet implemented
'''

class Game():
    def __init__(self, players):
        self.players = players
        self.round   = 1
        self.message = None

    def render(self):
        return (
            "", # content
            [discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED, color = config.Color.ERROR)], # embeds
            discord.View(), # view
            None, # file
            None # attachment
        )

    class Player:
        def __init__(self, id, name):
            self.id   = id
            self.name = name
            self.game = None

    class Achievement(Enum):
        

        def __new__(cls, value, description, emoji):
            obj = object.__new__(cls)
            obj._value_ = value

            obj.description = description
            obj.emoji = emoji

            return obj