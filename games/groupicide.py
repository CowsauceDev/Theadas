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

import random, copy, pickle, os
from enum import Enum
from typing import List

name = "Groupicide"

description = '''
    Take turns firing your gun until only one person is left alive!
'''

class Player():
    def __init__(self, id, name) -> None:
        self.id: int = id
        self.name: str = name

        self.bullets: int = 9

class Game():
    def __init__(self, players: List[Player]):
        self.players: List[Player] = players
        self.losers:  List[Player] = []

        self.message: discord.Message = None
        self.active: Player = random.choice(self.players)
        self.killed: bool = False

        for i in self.players:
            user = User(i.id)
            user.endorses_given = []
            user.claimed = False

            user.save()
        self.save()

    def save(self):
        game = copy.copy(self)
        game.message = None
        game.card = None

        for i in self.players: pickle.dump(game, open(f"{os.path.join(os.path.dirname(config.__file__), 'data/games')}/{i.id}.p", "wb"))

    def render(self):
        view = discord.ui.View()
        loadedButton = discord.ui.Button(emoji = "💥", label = "FIRE HERE")
        safeButton   = discord.ui.Button(emoji = "💥", label = "FIRE HERE")

        async def loadedCallback(interaction: discord.Interaction):
            await interaction.response.defer()
            if interaction.user.id != self.active.id:
                await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.WRONG_TURN.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                return
            else:
                index = self.players.index(self.active)
                self.losers.append(self.players.pop(self.active))
                self.active = self.active[self.players[index + 1 if index < len(self.players) - 1 else 0]]
                self.killed = True

            if len(self.players) == 1:
                endorseSelect = discord.ui.Select(placeholder = "Endorse a player.", row = 0)
                claimButton   = discord.ui.Button(emoji = "🎁", label = "CLAIM REWARDS", style = discord.ButtonStyle.green, row = 1)
                v = discord.ui.View(endorseSelect, claimButton)

                for i in self.players + self.losers: 
                    endorseSelect.add_option(label = i.name, value = i.name)
                    pickle.dump(None, open(f"{os.path.join(os.path.dirname(config.__file__), 'data/games')}/{i.id}.p", "wb"))

                async def endorseCallback(interaction):
                    await interaction.response.defer(ephemeral = True)

                    if interaction.user.id not in [i.id for i in self.players] and interaction.user.id not in [i.id for i in self.losers]: 
                        await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = "❌ Only people who played in the game can endorse or give medals.", color = config.Color.ERROR).set_footer(text = f"Version: {config.version}"))
                        return
                    
                    if interaction.user.name == endorseSelect.values[0]:
                        await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.GENERIC.value, color = config.Color.ERROR).set_footer(text = f"Version: {config.version}"), ephemeral = True)
                        return

                    for i in self.players + self.losers:
                        if i.name == endorseSelect.values[0]:
                            if i.name in User(interaction.user.id).endorses_given: 
                                await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.ALREADY_DID_THAT.value, color = config.Color.ERROR).set_footer(text = f"Version: {config.version}"))
                                return
                            
                            user = User(i.id)
                            user.endorsements += 1
                            user.save()
                            
                            u = User(interaction.user.id)
                            u.endorses_given.append(i.name)
                            u.save()

                            await interaction.followup.send(embed = discord.Embed(title = f"You endorsed {i.name}.", color = config.Color.COLORLESS), ephemeral = True)

                async def claimCallback(interaction):
                    await interaction.response.defer(ephemeral = True)

                    if interaction.user.id not in [i.id for i in self.players] and interaction.user.id not in [i.id for i in self.losers]: 
                        await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = "❌ Only people who played in the game can claim rewards from it.", color = config.Color.ERROR).set_footer(text = f"Version: {config.version}"))
                        return
                    
                    if User(interaction.user.id).claimed: 
                        await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.ALREADY_DID_THAT.value, color = config.Color.ERROR).set_footer(text = f"Version: {config.version}"), ephemeral = True)
                        return
                    
                    user = User(interaction.user.id)
                    xp, tickets, jackpot = user.award(interaction.user.id == self.players[0].id)

                    await interaction.followup.send(embed = discord.Embed(title = "You claimed your Rewards!", description = f"You received **{xp}** experience and **{tickets}** tickets." + (f"\n**JACKPOT!**\nYou also got {jackpot}!" if jackpot else ""), color = config.Color.COLORLESS), ephemeral = True)

                endorseSelect.callback, claimButton.callback = endorseCallback, claimCallback

                await self.message.delete()
                await interaction.followup.send(embed = discord.Embed(title = f"{self.players[0].name} wins!", description = "Endorse players below.", color = config.Color.COLORLESS))
            else:
                e, v = self.render()
                await self.message.delete()
                self.message = await interaction.followup.send(embed = e, view = v)

        async def safeCallback(interaction: discord.Interaction):
            await interaction.response.defer()
            if interaction.user.id != self.active.id:
                await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.WRONG_TURN.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                return
            else:
                self.active.bullets -= 1
                self.killed = False

                e, v = self.render()
                await self.message.delete()
                self.message = await interaction.followup.send(embed = e, view = v)

        loadedButton.callback, safeButton.callback = loadedCallback, safeCallback
        buttons: List[List[discord.ui.Button]] = [[] * 3]

        c = 0
        r = 0

        for _ in range(self.active.bullets):
            if c < 2:
                c += 1

                b = safeButton
                b.row = r
                buttons[r].append(b)
            else:
                r += 1
                c = 0

                b = safeButton
                b.row = r
                buttons[r].append(b)

        loadedButton.row = random.randint(0, 2)
        buttons[loadedButton.row][random.randint(0, 2)] = loadedButton

        for x in range(3):
            for y in range(3):
                b = buttons[x][y]
                b.row = x
                view.add_item(b)
        
        return discord.Embed(title = "Groupicide!", description = ("BANG! You died!\n" if self.killed else "") + f"It is now <@{self.active.id}>'s turn."), view

    class Achievement(Enum):
        

        def __new__(cls, value, description, emoji):
            obj = object.__new__(cls)
            obj._value_ = value

            obj.description = description
            obj.emoji = emoji

            return obj