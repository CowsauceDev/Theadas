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

import random
from enum import Enum
from typing import List

name = "Tic Tac Toe"

description = '''
    Take turns placing and X or O on the grid until you get 3 in a row!
'''

class Button(discord.ui.Button):
    def __init__(self, game, x: int, y: int, value: int):
        value = "X" if value == 1 else ("O" if value == -1 else "\u200b")

        super().__init__(style = discord.ButtonStyle.secondary, label = value, row = y)
        self.disabled = value != "\u200b" or game.winners()
        
        self.game = game
        self.value: str = value

        self.x: int = x
        self.y: int = y

        async def callback(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral = False)
            if interaction.user.id != game.a.id: await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.WRONG_TURN.value, color = config.Color.ERROR).set_footer(text = f"Version: {config.version}"), ephemeral = True)
            elif game.a == game.x: 
                game.board[self.x][self.y] = 1
                game.a = game.o

                c, v = game.render()
                await game.message.edit(content = c, view = v)
            
            elif game.a == game.o: 
                game.board[self.x][self.y] = -1
                game.a = game.x

                c, v = game.render()
                await game.message.edit(content = c, view = v)

        self.callback = callback

class Game():
    def __init__(self, users: User):
        self.users: User = users
        self.message: discord.Message = None

        self.a: User = random.choice(self.users)
        self.x: User = users[0]
        self.o: User = users[1]

        self.board: List[List[int]] = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

    def winners(self) -> List[User]:
        for i in self.board:
            if sum(i) == 3: return [self.x]
            elif sum(i) == -3: return [self.o]

        for i in range(3):
            if sum([self.board[0][i], self.board[1][i], self.board[2][i]]) == 3: return [self.x]
            if sum([self.board[0][i], self.board[1][i], self.board[2][i]]) == -3: return [self.o]
        
        if sum([self.board[0][2], self.board[1][1], self.board[2][0]]) == 3 or sum([self.board[0][0], self.board[1][1], self.board[2][2]]) == 3: return [self.x]
        if sum([self.board[0][2], self.board[1][1], self.board[2][0]]) == -3 or sum([self.board[0][0], self.board[1][1], self.board[2][2]]) == -3: return [self.o]
        
        if all(i != 0 for i in [self.board[x][y] for x in range(3) for y in range(3)]): return [self.x, self.o]

        return None

    def render(self):
        view = discord.ui.View()
        
        for x in range(3):
            for y in range(3):
                view.add_item(Button(self, x, y, self.board[x][y]))

        if self.winners():
            if len(self.winners()) > 1: return "It's a cat's game!", view
            else: return f"<@{self.winners()[0].id}> wins!", view
        else: return f"<@{self.a.id}>'s Turn", view

    class Achievement(Enum):
        

        def __new__(cls, value, description, emoji):
            obj = object.__new__(cls)
            obj._value_ = value

            obj.description = description
            obj.emoji = emoji

            return obj