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
import random, json, copy, os, pickle

from enum import Enum
from typing import List

name = "White on Black"

description = '''
    someone remind me to write this
'''

class Expansion(Enum):
    BASE = "Base Set"

class Card:
    def __init__(self, name, id, blanks):
        self.name = name
        self.id = id
        
        self.blanks = blanks

class Player:
    def __init__(self, id, name):
        self.id = id
        self.name: str = name

        self.mulled:   bool = False
        self.conceded: bool = False

        self.hand: List[Card] = []
        self.points: int = 0

    def draw(self, game, n):
        whites = game.whites
        if len(whites) <= 0: 
            wd = json.load(open("data/whiteonblack_cards/whites.json"))
            whites = [Card(i, str(wd.index(i)), None) for i in wd]
            random.shuffle(whites)

        for _ in range(n):
            card = random.choice(whites)
            card = whites.pop(whites.index(card))
            self.hand.append(card)
        return self.hand[-1]
    
    def play(self, game,  card = None, index = None):
        if card: index = self.hand.index(card)

        game.plays[self.id].append(self.hand.pop(index))
        self.draw(game, 1)

        game.save()

class Game():
    def __init__(self, players):
        self.players: List[Player] = players
        self.losers:  List[Player] = []

        self.message: discord.Message = None
        self.rounder: str = None
        self.czar: Player = random.choice(players)
        self.round: int = 1

        wd = json.load(open("data/whiteonblack_cards/whites.json"))
        bd = json.load(open("data/whiteonblack_cards/blacks.json"))

        self.blacks: List[Card] = [Card(i["name"], str(bd.index(i)), i["blanks"]) for i in bd]
        self.whites: List[Card] = [Card(i, str(wd.index(i)), None) for i in wd]
        self.plays:  dict  = {}

        random.shuffle(self.blacks)
        random.shuffle(self.whites)

        self.black: Card = self.blacks.pop(random.randint(0, len(self.blacks) - 1))

        for i in self.players:
            user = User(i.id)
            user.medals_given = []
            user.endorses_given = []
            user.claimed = False
            user.save()

            self.plays[i.id] = []
            i.draw(self, 10)
        self.save()
    
    def save(self):
        game = copy.copy(self)
        game.message = None
        for i in self.players: pickle.dump(game, open(f"{os.path.join(os.path.dirname(config.__file__), 'data/games')}/{i.id}.p", "wb"))

    def render(self):
        embeds = [discord.Embed(color = config.Color.BLACK_CARD, title = self.black.name)]
        content = f">>> **Round:** {self.round} | **Last Winner:** {self.rounder}\n"
        view = discord.ui.View(timeout = None)
        
        for i in self.players: content += f"\n**{i.name}:** {i.points} points" + ((" (Ready)" if len(self.plays[i.id]) == self.black.blanks else " (Not ready)") if i.id != self.czar.id else " (Czar)")
        for p in self.plays.keys():
            if len(self.plays[p]) > 0:
                s = ""
                for i in self.plays[p]: 
                    s += i.name if len(s) == 0 else f" | {i.name}"
                embeds.append(discord.Embed(description = s, color = config.Color.WHITE_CARD))

        playButton     = discord.ui.Button(style = discord.ButtonStyle.secondary, emoji = "🃏", label = "PLAY A CARD", row = 0)
        chooseButton   = discord.ui.Button(style = discord.ButtonStyle.secondary, emoji = "🎖️", label = "CHOOSE A WINNER", row = 0)
        mulliganButton = discord.ui.Button(style = discord.ButtonStyle.secondary, emoji = "♻️", label = "MULLIGAN", row = 1)
        concedeButton  = discord.ui.Button(style = discord.ButtonStyle.secondary, emoji = "🏳️", label = "CONCEDE", row = 1)

        async def playCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user.id == self.czar.id:
                e = discord.Embed()
                e.title = random.choice(config.error_titles)
                e.color = config.Color.ERROR
                e.description = config.Error.CZAR.value
                e.set_footer(text = config.footer)

                await interaction.followup.send(embed = e, ephemeral = True)

            elif len(self.plays[interaction.user.id]) >= self.black.blanks:
                e = discord.Embed()
                e.title = random.choice(config.error_titles)
                e.color = config.Color.ERROR
                e.description = config.Error.ALREADY_DID_THAT.value
                e.set_footer(text = config.footer)

                await interaction.followup.send(embed = e, ephemeral = True)

            else: 
                player = None
                embeds = []
                select = discord.ui.Select(placeholder = f"CHOOSE A CARD TO PLAY")
                v = discord.ui.View(timeout = None)

                for i in self.players: 
                    if i.id == interaction.user.id: player = i
                for i in player.hand:
                    embeds.append(discord.Embed(color = config.Color.WHITE_CARD, title = i.name))
                    select.add_option(label = i.name[0:100], value = i.id)

                async def selectCallback(interaction):
                    await interaction.response.defer(ephemeral = True)
                    card = None
                    for i in player.hand:
                        if i.id == select.values[0]: card = i

                    player.play(self, card = card)

                    c, e, v = self.render()
                    await self.message.delete()
                    self.message = await interaction.followup.send(content = c, embeds = e, view = v)
                                
                select.callback = selectCallback
                v.add_item(select)
                
                message = await interaction.followup.send(embeds = embeds, view = v, ephemeral = True)

        async def chooseCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user.id != self.czar.id:
                e = discord.Embed()
                e.title = random.choice(config.error_titles)
                e.color = config.Color.ERROR
                e.description = config.Error.NOT_CZAR.value
                e.set_footer(text = config.footer)

                await interaction.followup.send(embed = e, ephemeral = True)
                
            else: 
                select = discord.ui.Select(placeholder = f"CHOOSE A WINNER")
                v = discord.ui.View(timeout = None)

                for p in self.plays.keys():
                    if p != self.czar.id:
                        s = ""
                        for i in self.plays[p]:
                            s += i.name if len(s) == 0 else f" | {i.name}"
                        select.add_option(label = s[0:100], value = str(p))

                async def selectCallback(interaction):
                    await interaction.response.defer(ephemeral = True)
                    index = self.players.index(self.czar)

                    if len(self.blacks) <= 0: 
                        bd = json.load(open("data/whiteonblack_cards/blacks.json"))
                        self.blacks = [Card(i["name"], str(bd.index(i)), i["blanks"]) for i in bd]
                        random.shuffle(self.blacks)

                    for i in self.players:
                        i.mulled = False
                        self.plays[i.id] = []

                        if str(i.id) == select.values[0]: 
                            i.points += 1
                            self.rounder = f"{i.name} ({self.black.name})"

                    self.round += 1
                    self.black = self.blacks.pop(random.randint(0, len(self.blacks) - 1))
                    self.czar = self.players[index + 1 if index < len(self.players) - 1 else 0]

                    self.save()

                    c, e, v = self.render()
                    await message.delete()
                    self.message = await interaction.followup.send(content = c, embeds = e, view = v)
                                
                select.callback = selectCallback
                v.add_item(select)
                
                message = await interaction.followup.send(view = v, ephemeral = True)
        
        async def mulliganCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            player = None
            for i in self.players:
                if i.id == interaction.user.id: player = i
 
            if player.mulled:
                e = discord.Embed()
                e.title = random.choice(config.error_titles)
                e.color = config.Color.ERROR
                e.description = config.Error.ALREADY_DID_THAT.value
                e.set_footer(text = config.footer)

                await interaction.followup.send(embed = e, ephemeral = True)
            
            else:
                embeds = []
                message = None
                select = discord.ui.Select(placeholder = f"CHOOSE A CARD TO REPLACE")
                v = discord.ui.View(timeout = None)

                for i in player.hand: 
                    embeds.append(discord.Embed(color = config.Color.WHITE_CARD, title = i.id))
                    select.add_option(label = i.name[0:100], value = i.id)

                async def selectCallback(interaction):
                    await interaction.response.defer(ephemeral = True)
                    card = None

                    for i in player.hand:
                        if i.id == select.values[0]: card = i

                    old = player.hand.pop(player.hand.index(card)).name
                    new = player.draw(self, 1).name
                    player.mulled = True

                    for i in self.players: self.save()

                    await message.edit(embed = discord.Embed(description = f"You replaced \"{old[0:100]}\" with \"{new[0:100]}\"", color = config.Color.COLORLESS), view = discord.ui.View())
                                
                select.callback = selectCallback
                v.add_item(select)
                
                message = await interaction.followup.send(embeds = embeds, view = v, ephemeral = True)

        async def concedeCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            player = None

            for i in self.players:
                if i.id == interaction.user.id: player = i
            
            for i in player.hand: self.whites.append(i)
            random.shuffle(self.whites)

            self.losers.append(self.players.pop(self.players.index(player)))

            user = User(player.id)
            user.stats["whiteonblack"]["games"] += 1
            user.save()
            pickle.dump(None, open(f"{os.path.join(os.path.dirname(config.__file__), 'data/games')}/{user.id}.p", "wb"))

            if len(self.players) > 1: await interaction.followup.send(embed = discord.Embed(title = "You have conceded!", description = "You have been removed from the game and your cards have been shuffled back into the deck.", color = config.Color.COLORLESS))
            else:
                user = User(self.players[0].id)
                user.stats["whiteonblack"]["games"] += 1
                user.save()
                pickle.dump(None, open(f"{os.path.join(os.path.dirname(config.__file__), 'data/games')}/{user.id}.p", "wb"))

                medalSelect   = discord.ui.Select(placeholder = "Give a player a medal.", row = 1)
                endorseSelect = discord.ui.Select(placeholder = "Endorse a player.", row = 2)
                claimButton   = discord.ui.Button(emoji = "🎁", label = "CLAIM REWARDS", style = discord.ButtonStyle.green, row = 3)
                v = discord.ui.View(medalSelect, endorseSelect, claimButton)

                for i in self.players + self.losers: 
                    medalSelect.add_option(label = i.name, value = i.name)
                    endorseSelect.add_option(label = i.name, value = i.name)

                async def medalCallback(interaction):
                    await interaction.response.defer(ephemeral = True)
                    user = None
                    message = None

                    if interaction.user.id not in [i.id for i in self.players] and interaction.user.id not in [i.id for i in self.losers]: 
                        await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = "❌ Only people who played in the game can endorse or give medals.", color = config.Color.ERROR))
                        return
                    
                    if interaction.user.name == medalSelect.values[0]:
                        await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.GENERIC.value, color = config.Color.ERROR), ephemeral = True)
                        return

                    for i in self.players + self.losers:
                        if i.name == medalSelect.values[0]:
                            if i.name in User(interaction.user.id).medals_given or len(User(interaction.user.id).medals_given) > User(interaction.user.id).endorses: 
                                await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.ALREADY_DID_THAT.value, color = config.Color.ERROR), ephemeral = True)
                                return
                            
                            user = User(i.id)
                            u = User(interaction.user.id)

                            u.medals_given.append(i.name)
                            u.save()

                    async def callback(interaction):
                        await interaction.response.defer(ephemeral = True)
                        match s.values[0]:
                            case "lucky": user.stats["whiteonblack"]["medals"]["lucky"] += 1
                            case "nasty": user.stats["whiteonblack"]["medals"]["nasty"] += 1
                            case "funny": user.stats["whiteonblack"]["medals"]["funny"] += 1
                            case "offensive": user.stats["whiteonblack"]["medals"]["offensive"] += 1
                            case _: pass
                        
                        user.save()
                        await message.delete()

                    s = discord.ui.Select(placeholder = "PICK A MEDAL", options = [discord.SelectOption(label = "Lucky", description = "This player always seemed to draw the perfect card.", value = "lucky"), discord.SelectOption(label = "Nasty", description = "This person had the nastiest responses to almost every question, be it sexual or just plain gross.", value = "nasty"), discord.SelectOption(label = "Funny", description = "You could not get enough of this person\'s answers! What a wisecracker!", value = "funny"), discord.SelectOption(label = "Offensive", description = "How did they manage to make \"\" racist??", value = "offensive")])
                    s.callback = callback
                    v = discord.ui.View(s)

                    message = await interaction.followup.send(view = v, ephemeral = True)
                
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

                medalSelect.callback   = medalCallback
                endorseSelect.callback = endorseCallback
                claimButton.callback   = claimCallback

                await self.message.delete()
                self.message = await interaction.followup.send(embed = discord.Embed(title = f"{self.players[0].name} wins!", description = "Endorse players or award them medals below.", color = config.Color.COLORLESS), view = v)

        playButton.callback     = playCallback
        chooseButton.callback   = chooseCallback
        mulliganButton.callback = mulliganCallback
        concedeButton.callback  = concedeCallback

        for p in self.plays.keys():
            if p != self.czar.id:
                if len(self.plays[p]) < self.black.blanks:
                    view.add_item(playButton)
                    break
                view.add_item(chooseButton)

        view.add_item(mulliganButton)
        view.add_item(concedeButton)

        return content, embeds, view
    
    class Achievement(Enum):
        

        def __new__(cls, value, description, emoji):
            obj = object.__new__(cls)
            obj._value_ = value

            obj.description = description
            obj.emoji = emoji

            return obj