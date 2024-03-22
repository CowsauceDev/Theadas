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
from theadas import User, bot

import discord

import random, asyncio
from enum import Enum
from typing import List

name = "Quickdraw"

description = '''
    Be the first to draw your weapon, or be the first to hit the ground!
'''

class Game():
    def __init__(self, users: List[User]):
        self.users = users
        self.message: discord.Message = None

    def render(self):
        acceptButton = discord.ui.Button(label = "ACCEPT CHALLENGE", style = discord.ButtonStyle.secondary)

        async def acceptCallback(interaction):
            await interaction.response.defer(ephemeral = False)
            if interaction.user.id != self.users[1].id: await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.PERMISSION.value, color = config.Color.ERROR).set_footer(text = config.footer, ephemeral = True))
            else:
                await self.message.edit(embed = discord.Embed(title = f"{self.users[1].name} has accepted {self.users[0].name}'s challenge to a Quickdraw!", description = "A countdown has been started. After the countdown, a 💥 will appear, and the first player to click it wins!", color = config.Color.COLORLESS).set_footer(text = config.footer), view = discord.ui.View())
                await asyncio.sleep(random.randint(2, 15))
                await self.message.add_reaction("💥")

                try: _, u, = await bot.wait_for("reaction_add", check = lambda r, u: u in self.users and str(r.emoji) == "💥", timeout = 30)
                except asyncio.TimeoutError: await self.message.edit(embed = discord.Embed(title = f"☁️ Huh? No one drew in time.", color = config.Color.COLORLESS).set_footer(text = config.footer))
                else: 
                    await self.message.edit(embed = discord.Embed(title = f"💥 Bang! {u.name} draws first!", color = config.Color.COLORLESS).set_footer(text = config.footer))
                    await self.message.clear_reactions()

        acceptButton.callback = acceptCallback
        return discord.Embed(title = f"{self.users[0].name} has challenged {self.users[1].name} to a Quickdraw!", description = "When they accept the challenge, a countdown will start. After the countdown, a 💥 will appear, and the first player to click it wins!", color = config.Color.COLORLESS).set_footer(text = config.footer), discord.ui.View(acceptButton)

    class Achievement(Enum):
        

        def __new__(cls, value, description, emoji):
            obj = object.__new__(cls)
            obj._value_ = value

            obj.description = description
            obj.emoji = emoji

            return obj