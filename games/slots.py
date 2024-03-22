# Theadas Bot is a Discord bot allowing users to play various games with each other.
# Copyright © 2024 Jester (@cowsauce)

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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import config
from theadas import User

import discord

import random, asyncio
from enum import Enum
from typing import List

name = "Slot Machine"

description = '''
    Try your luck at the slot machine! Bet on which line you think can get 3 in a row and pull the lever to watch it spin!
'''

symbols: List[str] = [
    "7️⃣",
    "🍇",
    "🍒",
    "🍋",
    "🔔",
    "💎"
]

class Game():
    def __init__(self, user, bet, payline = 2):
        self.user: User = user
        self.bet: int = bet
        self.payline: int = payline

        self.rows: List[List[str]] = [[random.choice(symbols) for _ in range(3)] for _ in range(3)]
        self.started: bool = False
        self.stopped: bool = False

        self.message: discord.Message = None

    def board(self):
        board = "```\n-----------------"
        for row in self.rows:
            board += "\n: "
            for i in row: board += f"{i} : "
            if self.rows.index(row) == self.payline - 1: board += "<-"
        return board + "\n-----------------\n```"
    
    def won(self) -> bool: return self.stopped and (self.rows[self.payline - 1][0] == self.rows[self.payline - 1][1] == self.rows[self.payline - 1][2])

    def render(self):
        pullButton = discord.ui.Button(emoji = "🕹️", label = "PULL TO SPIN")
        stopButton = discord.ui.Button(emoji = "🕹️", label = "PULL TO STOP")

        async def pullCallback(interaction): 
            await interaction.response.defer(ephemeral = True)
            self.started = True

            while not self.stopped:
                for column in range(3):
                    self.rows[2][column], self.rows[1][column] = self.rows[1][column], self.rows[0][column]
                    self.rows[0][column] = random.choice(symbols)

                e, v = self.render()
                await self.message.edit(embed = e, view = v)
                await asyncio.sleep(0.5)

        async def stopCallback(interaction): 
            await interaction.response.defer(ephemeral = True)
            runs = random.randint(0, 3)

            while runs > 0:
                for column in range(3):
                    self.rows[2][column], self.rows[1][column] = self.rows[1][column], self.rows[0][column]
                    self.rows[0][column] = random.choice(symbols)

                runs -= 1
                e, v = self.render()
                await self.message.edit(embed = e, view = v)
                await asyncio.sleep(0.5)

            self.stopped = True
            if self.won(): self.user.chips += self.bet
            else: self.user.chips -= self.bet
            self.user.save()

            e, v = self.render()
            await self.message.edit(embed = e, view = discord.ui.View())

        pullButton.callback, stopButton.callback = pullCallback, stopCallback
        if self.started: view = discord.ui.View(stopButton)
        else: view = discord.ui.View(pullButton)

        return discord.Embed(title = f"🎰 Slot Machine ({self.bet} on line {self.payline})" + (" [WON!]" if self.won() else (" [LOST!]" if self.stopped else "")), description = self.board(), color = discord.Color.red() if self.stopped and not self.won() > 30 else (config.Color.SUCCESS if self.won() else config.Color.COLORLESS)).set_footer(text = config.footer), view

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