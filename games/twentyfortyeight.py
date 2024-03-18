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

import copy
import config
from theadas import User

import discord
import random, io

from typing import List
from enum import Enum
from PIL import Image, ImageDraw, ImageFont

name = "2048"

description = '''
    someone remind me to write this
'''

# board back: 0xbbada0
# blank tile: 0xcdc1b4
# dark font:  0x776e65
# light font: 0xf9f6f2

# 2: eee4da
# 4: ede0c8
# 8: f2b179
# 16: f59563
# 32: f67c5f
# 64: f65e3b
# 128: edcf72
# 256: edcc61
# 512: edc850
# 1024: edc53f
# 2048: edc22e
# big: 3c3a32

class Tile:
    def __init__(self, position: tuple[int, int], value: int = 0):
        self.position: tuple[int, int] = position
        self.value: int = value
        self.merged: bool = False

    def font(self) -> tuple[int, int, int]:
        return (119, 110, 101) if self.value < 8 else (249, 246, 242)

    def color(self) -> tuple[int, int, int]:
        match self.value:
            case 2:    return (238, 228, 218)
            case 4:    return (237, 224, 200)
            case 8:    return (242, 177, 121)
            case 16:   return (245, 149, 99)
            case 32:   return (246, 124, 95)
            case 64:   return (246, 94, 59)
            case 128:  return (237, 207, 114)
            case 256:  return (237, 204, 97)
            case 512:  return (237, 200, 80)
            case 1024: return (237, 197, 63)
            case 2048: return (237, 194, 46)
            case 0:    return (205, 193, 180)
            case _:    return (60, 58, 50)

class Game():
    def __init__(self, user):
        self.message: discord.Message = None
        self.user: User = user
        self.board: List[List[Tile]] = []
        self.user.plays["2048"] -= 1

        for x in range(4):
            row = []
            for y in range(4): row.append(Tile((x, y)))
            self.board.append(row)

        self.spawn(2)
    
    def spawn(self, n: int):
        spawns = 0

        while spawns < n:
            tile = random.choice(random.choice(self.board))
            value = 4 if random.randint(1, 10) == 1 else 2

            if tile.value == 0:
                tile.value = value
                spawns += 1

    def validate_move(self, direction: tuple[int, int]):
        board = copy.copy(self.board)

        # up
        if direction == (0, -1):
            for x in range(4):
                for y in range(3, -1, -1):
                    if y > 0 and (board[x][y].value != 0 and ((self.board[x][y - 1].merged == False and self.board[x][y].merged == False and board[x][y].value == board[x][y - 1].value) or board[x][y - 1].value == 0)): return True
            return False
        
        # down
        if direction == (0, 1):
            for x in range(4):
                for y in range(4):
                    try:
                        if board[x][y].value != 0 and ((self.board[x][y + 1].merged == False and self.board[x][y].merged == False and board[x][y].value == board[x][y + 1].value) or board[x][y + 1].value == 0): return True
                    except: pass
            return False
        
        # right
        if direction == (1, 0):
            for y in range(4):
                for x in range(3, -1, -1):
                    try:
                        if board[x][y].value != 0 and ((self.board[x + 1][y].merged == False and self.board[x][y].merged == False and board[x][y].value == board[x + 1][y].value) or board[x + 1][y].value == 0): return True
                    except: pass
            return False
        
        # left
        if direction == (-1, 0):
            for y in range(4):
                for x in range(4):
                    if x > 0 and (board[x][y].value != 0 and ((self.board[x - 1][y].merged == False and self.board[x][y].merged == False and board[x][y].value == board[x - 1][y].value) or board[x - 1][y].value == 0)): return True
            return False
    
    async def move(self, direction: tuple[int, int]):
        # while self.validate_move(direction):
        # up
        if direction == (0, -1):
            while self.validate_move(direction):
                for x in range(4):
                    for y in range(4):
                        if y > 0:
                            if self.board[x][y].value != 0 and self.board[x][y - 1].merged == False and self.board[x][y].merged == False and self.board[x][y].value == self.board[x][y - 1].value:
                                self.board[x][y - 1].value *= 2
                                self.board[x][y - 1].merged = True
                                self.board[x][y].value = 0

                            if self.board[x][y].value != 0 and self.board[x][y - 1].value == 0:
                                self.board[x][y - 1].value = self.board[x][y].value
                                self.board[x][y].value = 0
        
        # down
        if direction == (0, 1):
            while self.validate_move(direction):
                for x in range(4):
                    for y in range(3, -1, -1):
                        try:
                            if self.board[x][y].value != 0 and self.board[x][y + 1].merged == False and self.board[x][y].merged == False and self.board[x][y].value == self.board[x][y + 1].value:
                                self.board[x][y + 1].value *= 2
                                self.board[x][y + 1].merged = True
                                self.board[x][y].value = 0

                            if self.board[x][y].value != 0 and self.board[x][y + 1].value == 0:
                                self.board[x][y + 1].value = self.board[x][y].value
                                self.board[x][y].value = 0
                        except: pass
        
        # right
        if direction == (1, 0):
            while self.validate_move(direction):
                for y in range(4):
                    for x in range(3, -1, -1):
                        try:
                            if self.board[x][y].value != 0 and self.board[x + 1][y].merged == False and self.board[x][y].merged == False and self.board[x][y].value == self.board[x + 1][y].value:
                                self.board[x + 1][y].value *= 2
                                self.board[x + 1][y].merged = True
                                self.board[x][y].value = 0

                            if self.board[x][y].value != 0 and self.board[x + 1][y].value == 0:
                                self.board[x + 1][y].value = self.board[x][y].value
                                self.board[x][y].value = 0
                        except: pass
        
        # left
        if direction == (-1, 0):
            while self.validate_move(direction):
                for y in range(4):
                    for x in range(4):
                        if x > 0:
                            if self.board[x][y].value != 0 and self.board[x - 1][y].merged == False and self.board[x][y].merged == False and self.board[x][y].value == self.board[x - 1][y].value:
                                self.board[x - 1][y].value *= 2
                                self.board[x - 1][y].merged = True
                                self.board[x][y].value = 0

                            if self.board[x][y].value != 0 and self.board[x - 1][y].value == 0:
                                self.board[x - 1][y].value = self.board[x][y].value
                                self.board[x][y].value = 0

        if True not in [self.validate_move(i) for i in [(0, -1), (-1, 0), (1, 0), (0, 1)]]:
            self.user.stats["2048"]["games"] += 1
            self.user.save()

            e, _, f = self.render()
            e.set_image(url = "attachment://board.png").set_footer(text = config.footer).description = "You LOST! You ran out of space without getting 2048."
            await self.message.edit(embed = e, view = discord.ui.View(), file = f)
            return
        
        if 2048 in [self.board[x][y] for x in range(4) for y in range(4)]:
            self.user.stats["2048"]["games"] += 1
            self.user.save()

            e, _, f = self.render()
            e.set_image(url = "attachment://board.png").set_footer(text = config.footer).description = "You WON! Look at that shiny 2048 tile!"
            await self.message.edit(embed = e, view = discord.ui.View(), file = f)
            return

        self.spawn(1)
        for i in [self.board[x][y] for x in range(4) for y in range(4)]: i.merged = False

    def render(self):
        upButton    = discord.ui.Button(emoji = "🔼", style = discord.ButtonStyle.secondary, row = 0, disabled = not self.validate_move((0, -1)))
        leftButton  = discord.ui.Button(emoji = "◀️", style = discord.ButtonStyle.secondary, row = 1, disabled = not self.validate_move((-1, 0)))
        rightButton = discord.ui.Button(emoji = "▶️", style = discord.ButtonStyle.secondary, row = 1, disabled = not self.validate_move((1, 0)))
        downButton  = discord.ui.Button(emoji = "🔽", style = discord.ButtonStyle.secondary, row = 2, disabled = not self.validate_move((0, 1)))
        
        view = discord.ui.View(
            discord.ui.Button(emoji = "🟦", style = discord.ButtonStyle.secondary, row = 0, disabled = True),
            upButton,
            discord.ui.Button(emoji = "🟦", style = discord.ButtonStyle.secondary, row = 0, disabled = True),
            leftButton,
            discord.ui.Button(emoji = "🟦", style = discord.ButtonStyle.secondary, row = 1, disabled = True),
            rightButton,
            discord.ui.Button(emoji = "🟦", style = discord.ButtonStyle.secondary, row = 2, disabled = True),
            downButton,
            discord.ui.Button(emoji = "🟦", style = discord.ButtonStyle.secondary, row = 2, disabled = True)
        )

        board_size = 620
        tilesize = 130
        margin = 20
        corner = 10

        board = Image.new("RGB", (board_size, board_size), (187, 173, 160))
        bytes = io.BytesIO()

        for row in self.board:
            for i in row:
                coords = (margin + ((tilesize + margin) * (i.position[0])), margin + ((tilesize + margin) * (i.position[1])))
                font = ImageFont.truetype("times", 100)

                draw = ImageDraw.Draw(board)
                draw.rounded_rectangle(xy = (coords[0], coords[1], coords[0] + tilesize, coords[1] + tilesize), radius = corner,  fill = i.color())

                if i.value > 0: draw.text(xy = (coords[0] + (tilesize / 2), coords[1] + (tilesize / 2)), text = str(i.value), fill = i.font(), font = font, anchor = "mm")

        board.save(bytes, "png")
        bytes.seek(0)

        async def upCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            await self.move((0, -1))

            e, v, f = self.render()
            await self.message.edit(embed = e, view = v, file = f)

        async def leftCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            await self.move((-1, 0))

            e, v, f = self.render()
            await self.message.edit(embed = e, view = v, file = f)

        async def rightCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            await self.move((1, 0))

            e, v, f = self.render()
            await self.message.edit(embed = e, view = v, file = f)

        async def downCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            await self.move((0, 1))

            e, v, f = self.render()
            await self.message.edit(embed = e, view = v, file = f)

        upButton.callback, leftButton.callback, rightButton.callback, downButton.callback = upCallback, leftCallback, rightCallback, downCallback
        return discord.Embed(color = config.Color.COLORLESS).set_image(url = "attachment://board.png").set_footer(text = config.footer), view, discord.File(fp = bytes, filename = "board.png")
    
    class Achievement(Enum):
        

        def __new__(cls, value, description, emoji):
            obj = object.__new__(cls)
            obj._value_ = value

            obj.description = description
            obj.emoji = emoji

            return obj