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

import copy, os, pickle, random, math
from collections import Counter
from enum import Enum
from typing import List

name = "BAMBOOZLE! [beta]"

description = '''
    This game is not yet implemented
'''

class Player:
    def __init__(self, id: int, name: str):
        self.id: int = id
        self.name: str = name

        self.alignment: int = 0
        self.role: Role = None

        self.dead: bool = False
        self.revealed: bool = False

class ActionButtons:
    async def passCallback(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral = True)

        user = User(interaction.user.id)
        game = user.game()
        player = None

        for i in game.players:
            if i.id == user.id: player = i

        player.night_acted = True
        game.save()

        await interaction.followup.send(embed = discord.Embed(title = "You have forfeited your night action. You will not do it this night.", color = config.Color.SUCCESS).set_footer(text = config.footer))
        
    async def investigateCallback(interaction: discord.Interaction): await interaction.response.defer()
    async def tamperCallback(interaction: discord.Interaction): await interaction.response.defer()
    async def lightsCallback(interaction: discord.Interaction): await interaction.response.defer()
    async def gaurdCallback(interaction: discord.Interaction): await interaction.response.defer()
    async def swapCallback(interaction: discord.Interaction): await interaction.response.defer()
    async def seeCallback(interaction: discord.Interaction): await interaction.response.defer()
    async def reviveCallback(interaction: discord.Interaction): await interaction.response.defer()
    async def killCallback(interaction: discord.Interaction): await interaction.response.defer()

    passButton = discord.ui.Button()
    passButton.callback = passCallback

    investigateButton = discord.ui.Button()
    investigateButton.callback = investigateCallback

    tamperButton = discord.ui.Button()
    tamperButton.callback = tamperCallback

    lightsButton = discord.ui.Button()
    lightsButton.callback = lightsCallback

    gaurdButton = discord.ui.Button()
    gaurdButton.callback = gaurdCallback

    swapButton = discord.ui.Button()
    swapButton.callback = swapCallback

    seeButton = discord.ui.Button()
    seeButton.callback = seeCallback

    reviveButton = discord.ui.Button()
    reviveButton.callback = reviveCallback

    killButton = discord.ui.Button()
    killButton.callback = killCallback

class Role(Enum):
    WEREWOLF             = ("Werewolf", "https://media.istockphoto.com/id/1153852267/vector/playing-card-joker-yellow-red-blue-black.jpg?s=612x612&w=0&k=20&c=Hgz0isA2JMM-q6zOSND372GmFTFzP6HZKYD_tVWK5rk=")
    WEREWOLF_DETECTIVE   = ("Werewolf Detective", "https://media.istockphoto.com/id/1153852267/vector/playing-card-joker-yellow-red-blue-black.jpg?s=612x612&w=0&k=20&c=Hgz0isA2JMM-q6zOSND372GmFTFzP6HZKYD_tVWK5rk=")
    TAMPERING_WOLF       = ("Tampering Wolf", "https://media.istockphoto.com/id/1153852267/vector/playing-card-joker-yellow-red-blue-black.jpg?s=612x612&w=0&k=20&c=Hgz0isA2JMM-q6zOSND372GmFTFzP6HZKYD_tVWK5rk=")
    WEREWOLF_ELECTRICIAN = ("Werewolf Electrician", "https://media.istockphoto.com/id/1153852267/vector/playing-card-joker-yellow-red-blue-black.jpg?s=612x612&w=0&k=20&c=Hgz0isA2JMM-q6zOSND372GmFTFzP6HZKYD_tVWK5rk=")
    WEREWOLF_SCOUT       = ("Werewolf Scout", "https://media.istockphoto.com/id/1153852267/vector/playing-card-joker-yellow-red-blue-black.jpg?s=612x612&w=0&k=20&c=Hgz0isA2JMM-q6zOSND372GmFTFzP6HZKYD_tVWK5rk=")

    VILLAGER             = ("Villager", "https://media.istockphoto.com/id/1153852267/vector/playing-card-joker-yellow-red-blue-black.jpg?s=612x612&w=0&k=20&c=Hgz0isA2JMM-q6zOSND372GmFTFzP6HZKYD_tVWK5rk=")
    DETECTIVE            = ("Detective", "https://media.istockphoto.com/id/1153852267/vector/playing-card-joker-yellow-red-blue-black.jpg?s=612x612&w=0&k=20&c=Hgz0isA2JMM-q6zOSND372GmFTFzP6HZKYD_tVWK5rk=")
    GAURD                = ("Gaurd", "https://media.istockphoto.com/id/1153852267/vector/playing-card-joker-yellow-red-blue-black.jpg?s=612x612&w=0&k=20&c=Hgz0isA2JMM-q6zOSND372GmFTFzP6HZKYD_tVWK5rk=")
    SCOUT                = ("Scout", "https://media.istockphoto.com/id/1153852267/vector/playing-card-joker-yellow-red-blue-black.jpg?s=612x612&w=0&k=20&c=Hgz0isA2JMM-q6zOSND372GmFTFzP6HZKYD_tVWK5rk=")
    MAGICIAN             = ("Magician", "https://media.istockphoto.com/id/1153852267/vector/playing-card-joker-yellow-red-blue-black.jpg?s=612x612&w=0&k=20&c=Hgz0isA2JMM-q6zOSND372GmFTFzP6HZKYD_tVWK5rk=")
    SEER                 = ("Seer", "https://media.istockphoto.com/id/1153852267/vector/playing-card-joker-yellow-red-blue-black.jpg?s=612x612&w=0&k=20&c=Hgz0isA2JMM-q6zOSND372GmFTFzP6HZKYD_tVWK5rk=")
    WITCH_DOCTOR         = ("Witch Doctor", "https://media.istockphoto.com/id/1153852267/vector/playing-card-joker-yellow-red-blue-black.jpg?s=612x612&w=0&k=20&c=Hgz0isA2JMM-q6zOSND372GmFTFzP6HZKYD_tVWK5rk=")
    NINJA                = ("Ninja", "https://media.istockphoto.com/id/1153852267/vector/playing-card-joker-yellow-red-blue-black.jpg?s=612x612&w=0&k=20&c=Hgz0isA2JMM-q6zOSND372GmFTFzP6HZKYD_tVWK5rk=")
    ICER                 = ("Icer", "https://media.istockphoto.com/id/1153852267/vector/playing-card-joker-yellow-red-blue-black.jpg?s=612x612&w=0&k=20&c=Hgz0isA2JMM-q6zOSND372GmFTFzP6HZKYD_tVWK5rk=")
    GLORIOUS_CHAIRMAN    = ("Glorious Chairman", "https://media.istockphoto.com/id/1153852267/vector/playing-card-joker-yellow-red-blue-black.jpg?s=612x612&w=0&k=20&c=Hgz0isA2JMM-q6zOSND372GmFTFzP6HZKYD_tVWK5rk=")
    HARLOT               = ("Harlot", "https://media.istockphoto.com/id/1153852267/vector/playing-card-joker-yellow-red-blue-black.jpg?s=612x612&w=0&k=20&c=Hgz0isA2JMM-q6zOSND372GmFTFzP6HZKYD_tVWK5rk=")

    TANNER               = ("Tanner", "https://media.istockphoto.com/id/1153852267/vector/playing-card-joker-yellow-red-blue-black.jpg?s=612x612&w=0&k=20&c=Hgz0isA2JMM-q6zOSND372GmFTFzP6HZKYD_tVWK5rk=")
    SERIAL_KILLER        = ("Serial Killer", "https://media.istockphoto.com/id/1153852267/vector/playing-card-joker-yellow-red-blue-black.jpg?s=612x612&w=0&k=20&c=Hgz0isA2JMM-q6zOSND372GmFTFzP6HZKYD_tVWK5rk=")
    GAURDIAN_ANGEL       = ("Gaurdian Angel", "https://media.istockphoto.com/id/1153852267/vector/playing-card-joker-yellow-red-blue-black.jpg?s=612x612&w=0&k=20&c=Hgz0isA2JMM-q6zOSND372GmFTFzP6HZKYD_tVWK5rk=")
    PLAGUE_DOCTOR        = ("Plague Doctor", "https://media.istockphoto.com/id/1153852267/vector/playing-card-joker-yellow-red-blue-black.jpg?s=612x612&w=0&k=20&c=Hgz0isA2JMM-q6zOSND372GmFTFzP6HZKYD_tVWK5rk=")

def __new__(cls, value, image):
    obj = object.__new__(cls)
    obj._value_ = value

    obj.title = value
    obj.image = image

    return obj

class Game():
    def __init__(self, players: List[Player]):
        self.players: List[Player] = players
        self.losers:  List[Player]  = []
        self.winners: List[Player]  = []

        self.message: discord.Message = None
        self.log: str = ""

        self.round: int = 1
        self.priority: int = 1

        self.votes: dict = {}
        self.kill_votes: dict = {}

        for i in players:
            self.votes[i.id] = None
            user = User(i.id)

            user.medals_given = []
            user.endorses_given = []
            user.claimed = False

            user.save()

        for i in self.wolves(): self.kill_votes[i.id] = None
    
    def save(self):
        game = copy.copy(self)
        game.message = None

        for i in self.players: pickle.dump(game, open(f"{os.path.join(os.path.dirname(config.__file__), 'data/games')}/{i.id}.p", "wb"))

    def villages(self) -> List[Player]: return [i for i in self.players if i.alignment == 0]
    def wolves(self) -> List[Player]: return [i for i in self.players if i.alignment == 1]
    def self_aligned(self) -> List[Player]: return [i for i in self.players if i.alignment == 2]
    def is_night(self)-> bool: return self.round % 2 == 0
    def night_actors(self) -> List[Player]: return [i for i in self.players if i.role in [Role.GAURD, Role.MAGICIAN, Role.SEER, Role.TAMPERING_WOLF, Role.SERIAL_KILLER, Role.NINJA, Role.ICER, Role.HARLOT]]

    def render(self):
        if self.is_night():
            description = f"{self.log} It is currently **🌙 night**. If you have a night action, use it now. Click `🐺 KILL` to vote a player out or choose to abstain.\n## Rules:\n> 1) You MAY NOT show others your messages from this bot.\n> 2) Dead players MAY NOT speak (unless they are in a seance)\n"
            actionButton = discord.ui.Button(emoji = "💥", label = "TAKE NIGHT ACTION", disabled = None in [i for i in self.wolves() if self.kill_votes[i.id]])
            killButton   = discord.ui.Button(emoji = "🐺", label = "KILL")

            async def actionCallback(interaction: discord.Interaction):
                await interaction.response.defer(ephemeral = True)
                player: Player = None
                for i in self.players:
                    if i.id == interaction.user.id: player = i
                
                match player.role:
                    case Role.WEREWOLF_DETECTIVE: await interaction.response.followup.send(embed = discord.Embed(title = f"You are the {player.role}", description = "You can investigate 1 person each night to learn their role. Use the `🔎 INVESTIGATE` button to investigate someone. Use `PASS` to pass on investigating someone tonight.", color = config.Color.ERROR).set_footer(text = config.footer).set_image(url = player.role.image), view = discord.ui.View(ActionButtons.investigateButton, ActionButtons.passButton))
                    case Role.TAMPERING_WOLF: await interaction.response.followup.send(embed = discord.Embed(title = f"You are the {player.role}", description = "You can make someone's role card appear changed once per night. Use the `♻️ TAMPER` buttton to swap someone's role card.", color = config.Color.ERROR).set_footer(text = config.footer).set_image(url = player.role.image), view = discord.ui.View(ActionButtons.tamperButton, ActionButtons.passButton))
                    case Role.WEREWOLF_SCOUT: await interaction.response.followup.send(embed = discord.Embed(title = f"You are the {player.role}", description = "You have no night action but will be sent a list of people who leave their house each night.", color = config.Color.ERROR).set_footer(text = config.footer).set_image(url = player.role.image))
                    case Role.DETECTIVE: await interaction.response.followup.send(embed = discord.Embed(title = f"You are the {player.role}", description = "You can visit and investigate 1 person each night to learn their role. Use the `🔎 INVESTIGATE` button to investigate someone.", color = config.Color.ERROR).set_footer(text = config.footer).set_image(url = player.role.image), view = discord.ui.View(ActionButtons.investigateButton, ActionButtons.passButton))
                    case Role.GAURD: await interaction.response.followup.send(embed = discord.Embed(title = f"You are the {player.role}", description = "You can visit and guard 1 person each night to prevent anyone else from visiting them. Use the `🛡️ GUARD` button to guard someone.", color = config.Color.ERROR).set_footer(text = config.footer).set_image(url = player.role.image), view = discord.ui.View(ActionButtons.gaurdButton, ActionButtons.passButton))
                    case Role.SCOUT: await interaction.response.followup.send(embed = discord.Embed(title = f"You are the {player.role}", description = "You have no night action but will be sent a list of people who leave their house each night.", color = config.Color.ERROR).set_footer(text = config.footer).set_image(url = player.role.image))
                    case Role.MAGICIAN: await interaction.response.followup.send(embed = discord.Embed(title = f"You are the {player.role}", description = "You can visit and swap roles with 1 person each night. Use the `🪄 SWAP` button to swap with someone.", color = config.Color.ERROR).set_footer(text = config.footer).set_image(url = player.role.image), view = discord.ui.View(ActionButtons.swapButton, ActionButtons.passButton))
                    case Role.SEER: await interaction.response.followup.send(embed = discord.Embed(title = f"You are the {player.role}", description = "You can reveal someone's alignment every night without visiting them. Use the `🔮 SEE` button to see someone's alignment.", color = config.Color.ERROR).set_footer(text = config.footer).set_image(url = player.role.image), view = discord.ui.View(ActionButtons.seeButton, ActionButtons.passButton))
                    case Role.WITCH_DOCTOR: await interaction.response.followup.send(embed = discord.Embed(title = f"You are the {player.role}", description = "You can revive one dead player per game. Use the `⤴️ REVIVE` btton to revive someone.", color = config.Color.ERROR).set_footer(text = config.footer).set_image(url = player.role.image), view = discord.ui.View(ActionButtons.reviveButton, ActionButtons.passButton))
                    case Role.SERIAL_KILLER: await interaction.response.followup.send(embed = discord.Embed(title = f"You are the {player.role}", description = "You can visit and kill one person per night. Use the `🗡️ KILL` btton to kill someone.", color = config.Color.ERROR).set_footer(text = config.footer).set_image(url = player.role.image), view = discord.ui.View(ActionButtons.killButton, ActionButtons.passButton))
                    case _: await interaction.response.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NO_ACTION, color = config.Color.ERROR).set_footer(text = config.footer))

            async def killCallback(interaction):
                await interaction.response.defer(ephemeral = True)
                message: discord.Message = None
                select = discord.ui.Select(placeholder = "PLAYERS", options = [discord.SelectOption(label = i.name, value = i.id) for i in self.players] + "abstain")

                for i in self.players:
                    if i.id == interaction.user.id:
                        p = i
                        if p.dead:
                            await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.DEAD.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                            return
                        elif i.alignment != 1:
                            await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.CANT_KILL.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                            return

                async def selectCallback(interaction):
                    await interaction.response.defer(ephemeral = False)
                    killer: Player = None
                    killed: Player = None

                    for i in self.players:
                        if i.id == interaction.user.id: killer = i
                        if i.id == select.values[0]:    killed = i

                    self.votes[killer.id] = killed.id
                    if all(i.dead or self.votes[i.id] is not None for i in self.players):
                        loser = Counter([i for i in self.votes.values()]).most_common(1)[0]
                        if loser[0] == "abstain": 
                            for i in self.players: self.votes[i.id] = None
                            self.log = f"What's this? You can't find any evidence of the wolves killing last night."
                            self.round += 1
                            self.save()

                        else:
                            for i in self.players: 
                                self.votes[i.id] = None
                                if i.id == loser[0]: i.dead = True

                                if all(i.dead for i in self.wolves()):
                                    k = 80
                                    avg_winner_sr = sum([User(i.id).sr for i in self.winners])/len([User(i.id).sr for i in self.winners])
                                    avg_loser_sr  = sum([User(i.id).sr for i in self.losers])/len([User(i.id).sr for i in self.losers])

                                    e = 1 / (1 + 10**(avg_winner_sr - avg_loser_sr) / 400)

                                    for i in self.winners:
                                        winner = User(i.id)
                                        winner.stats["bamboozle"]["wins"] += 1
                                        winner.stats["bamboozle"]["sr"] += (k * (1 - e)) * 3 if i in self.wolves() else (k * (1 - e))
                                        
                                        winner.save()
                                    
                                    for i in self.losers:
                                        loser = User(i.id)
                                        loser.stats["bamboozle"]["losses"] += 1
                                        loser.stats["bamboozle"]["sr"] -= (k * (1 - e))
                                        
                                        loser.save()

                                    medalSelect   = discord.ui.Select(placeholder = "Give a player a medal.", row = 1)
                                    endorseSelect = discord.ui.Select(placeholder = "Endorse a player.", row = 2)
                                    claimButton   = discord.ui.Button(emoji = "🎁", label = "CLAIM REWARDS", style = discord.ButtonStyle.green, row = 3)
                                    v = discord.ui.View(medalSelect, endorseSelect, claimButton)

                                    for i in self.players: 
                                        medalSelect.add_option(label = i.name, value = i.name)
                                        endorseSelect.add_option(label = i.name, value = i.name)

                                        pickle.dump(None, open(f"{os.path.join(os.path.dirname(config.__file__), 'data/games')}/{i.id}.p", "wb"))

                                    async def medalCallback(interaction):
                                        await interaction.response.defer(ephemeral = True)
                                        user = None
                                        message = None

                                        if interaction.user.id not in [i.id for i in self.players]: 
                                            await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = "❌ Only people who played in the game can endorse or give medals.", color = config.Color.ERROR))
                                            return
                                        
                                        if interaction.user.name == medalSelect.values[0]:
                                            await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.GENERIC.value, color = config.Color.ERROR), ephemeral = True)
                                            return

                                        for i in self.players:
                                            if i.name == medalSelect.values[0]:
                                                user = User(i.id)
                                                u = User(interaction.user.id)

                                                if i.name in u.medals_given or len(u.medals_given) > u.endorses:
                                                    await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.ALREADY_DID_THAT.value, color = config.Color.ERROR), ephemeral = True)
                                                    return
                                                
                                                u.medals_given.append(i.name)
                                                u.save()

                                        async def callback(interaction):
                                            await interaction.response.defer(ephemeral = True)
                                            match s.values[0]:
                                                case "lucky": user.stats["trust"]["medals"]["lucky"] += 1
                                                case "smart investor": user.stats["trust"]["medals"]["smart investor"] += 1
                                                case "negotiator": user.stats["trust"]["medals"]["negotiator"] += 1
                                                case _: pass
                                            
                                            user.save()
                                            await message.delete()

                                        s = discord.ui.Select(placeholder = "PICK A MEDAL", options = [discord.SelectOption(label = "Lucky", description = "This player always seemed to roll perfectly.", value = "lucky"), discord.SelectOption(label = "Smart Investor", description = "This player knew what to buy and when to upgrade.", value = "smart investor"), discord.SelectOption(label = "Negotiator", description = "They always found clever trades that benefitted them the most.", value = "negotiator")])
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
                                    await interaction.followup.send(embed = discord.Embed(title = f"After {self.round} rounds, the game is over.", description = "- The townspeople won by killing all the wolves!" + ("\n- The **Tanner** also won by getting themselves killed!" if len([i for i in self.players if i.role == Role.TANNER and i.dead]) else "") + ("\n- The **Plague Doctor** also won by giving everyone the plague!" if Role.PLAGUE_DOCTOR in [i.role for i in self.players] and all(i.plague for i in self.players) else "") + ("\n- The **Guardian Angel** also won by helping their Protected survive!" if len([i.role == Role.GAURDIAN_ANGEL and not i.protecting.dead for i in self.players]) > 0 else "") + "\n\nEndorse players or award them medals below.", color = config.Color.COLORLESS), view = discord.ui.View(endorseSelect, medalSelect, claimButton))
                                    return
                                
                                elif all(i.dead for i in self.villagers()):
                                    k = 80
                                    avg_winner_sr = sum([User(i.id).sr for i in self.winners])/len([User(i.id).sr for i in self.winners])
                                    avg_loser_sr  = sum([User(i.id).sr for i in self.losers])/len([User(i.id).sr for i in self.losers])

                                    e = 1 / (1 + 10**(avg_winner_sr - avg_loser_sr) / 400)

                                    for i in self.winners:
                                        winner = User(i.id)
                                        winner.stats["bamboozle"]["wins"] += 1
                                        winner.stats["bamboozle"]["sr"] += (k * (1 - e)) * 3 if i in self.wolves() else (k * (1 - e))
                                        
                                        winner.save()
                                    
                                    for i in self.losers:
                                        loser = User(i.id)
                                        loser.stats["bamboozle"]["losses"] += 1
                                        loser.stats["bamboozle"]["sr"] -= (k * (1 - e))
                                        
                                        loser.save()

                                    medalSelect   = discord.ui.Select(placeholder = "Give a player a medal.", row = 1)
                                    endorseSelect = discord.ui.Select(placeholder = "Endorse a player.", row = 2)
                                    claimButton   = discord.ui.Button(emoji = "🎁", label = "CLAIM REWARDS", style = discord.ButtonStyle.green, row = 3)
                                    v = discord.ui.View(medalSelect, endorseSelect, claimButton)

                                    for i in self.players: 
                                        medalSelect.add_option(label = i.name, value = i.name)
                                        endorseSelect.add_option(label = i.name, value = i.name)

                                        pickle.dump(None, open(f"{os.path.join(os.path.dirname(config.__file__), 'data/games')}/{i.id}.p", "wb"))

                                    async def medalCallback(interaction):
                                        await interaction.response.defer(ephemeral = True)
                                        user = None
                                        message = None

                                        if interaction.user.id not in [i.id for i in self.players]: 
                                            await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = "❌ Only people who played in the game can endorse or give medals.", color = config.Color.ERROR))
                                            return
                                        
                                        if interaction.user.name == medalSelect.values[0]:
                                            await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.GENERIC.value, color = config.Color.ERROR), ephemeral = True)
                                            return

                                        for i in self.players:
                                            if i.name == medalSelect.values[0]:
                                                user = User(i.id)
                                                u = User(interaction.user.id)

                                                if i.name in u.medals_given or len(u.medals_given) > u.endorses:
                                                    await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.ALREADY_DID_THAT.value, color = config.Color.ERROR), ephemeral = True)
                                                    return
                                                
                                                u.medals_given.append(i.name)
                                                u.save()

                                        async def callback(interaction):
                                            await interaction.response.defer(ephemeral = True)
                                            match s.values[0]:
                                                case "lucky": user.stats["trust"]["medals"]["lucky"] += 1
                                                case "smart investor": user.stats["trust"]["medals"]["smart investor"] += 1
                                                case "negotiator": user.stats["trust"]["medals"]["negotiator"] += 1
                                                case _: pass
                                            
                                            user.save()
                                            await message.delete()

                                        s = discord.ui.Select(placeholder = "PICK A MEDAL", options = [discord.SelectOption(label = "Lucky", description = "This player always seemed to roll perfectly.", value = "lucky"), discord.SelectOption(label = "Smart Investor", description = "This player knew what to buy and when to upgrade.", value = "smart investor"), discord.SelectOption(label = "Negotiator", description = "They always found clever trades that benefitted them the most.", value = "negotiator")])
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
                                    await interaction.followup.send(embed = discord.Embed(title = f"After {self.round} rounds, the game is over.", description = "- The wolves won by killing all the townspeople!" + ("\n- The **Tanner** also won by getting themselves killed!" if len([i for i in self.players if i.role == Role.TANNER and i.dead]) else "") + ("\n- The **Plague Doctor** also won by giving everyone the plague!" if Role.PLAGUE_DOCTOR in [i.role for i in self.players] and all(i.plague for i in self.players) else "") + ("\n- The **Guardian Angel** also won by helping their Protected survive!" if len([i.role == Role.GAURDIAN_ANGEL and not i.protecting.dead for i in self.players]) > 0 else "") + "\n\nEndorse players or award them medals below.", color = config.Color.COLORLESS), view = discord.ui.View(endorseSelect, medalSelect, claimButton))
                                    return

                                self.log = f"🐺 The wolves have struck again! 🩸**<@{loser[0]}>** has been slain!"
                                self.round += 1
                                self.save()

                    self.save()
                    e, v = self.render()
                    await message.delete()

                    await self.message.delete()
                    self.message = await interaction.followup.send(embed = e, view = v, ephemeral = False)

                select.callback = selectCallback
                message = await interaction.response.followup.send(embed = discord.Embed(title = "The player with the most votes will die!", color = config.Color.COLORLESS).set_footer(text = config.footer), view = discord.ui.View(select))

            for i in self.players: description += f"\n- **<@{i.id}>**" + (" [DEAD]" if i.dead else " [ALIVE]") + (" [VOTED]" if self.votes[i.id] else " [VOTING]") + (f" ({i.role.title})" if i.dead or i.revealed else "")
            actionButton.callback, killButton.callback = actionCallback, killCallback

            return discord.Embed(title = f"BAMBOOZLE! | Day {math.ceil(self.round / 2)}", description = description, color = config.Color.BAMBOOZLE).set_footer(text = config.footer), discord.ui.View(actionButton, killButton)
        else:
            description = f"{self.log} It is currently **☀️ day**. If you have a day action, use it before everyone votes. Click `🗳️ VOTE` to vote a player out or choose to abstain.\n## Rules:\n> 1) You MAY NOT show others your messages from this bot.\n> 2) Dead players MAY NOT speak (unless they are in a seance)\n"
            actionButton = discord.ui.Button(emoji = "💥", label = "TAKE DAY ACTION", disabled = None in [i for i in self.players if self.votes[i.id]])
            voteButton   = discord.ui.Button(emoji = "🗳️", label = "VOTE")

            async def actionCallback(interaction):
                await interaction.response.defer(ephemeral = True)
                player: Player = None
                for i in self.players:
                    if i.id == interaction.user.id: player = i

                match player.role:
                    case Role.WITCH_DOCTOR: await interaction.response.followup.send(embed = discord.Embed(title = f"You are the {player.role}", description = "You can revive one dead player per game. Use the `⤴️ REVIVE` btton to revive someone.", color = config.Color.ERROR).set_footer(text = config.footer).set_image(url = player.role.image), view = discord.ui.View(ActionButtons.reviveButton, ActionButtons.passButton))
                    case Role.WEREWOLF_ELECTRICIAN: await interaction.response.followup.send(embed = discord.Embed(title = f"You are the {player.role}", description = "You can change day to night once per game. Use the `🌙 LIGHTS` button to kill the lights.", color = config.Color.ERROR).set_footer(text = config.footer).set_image(url = player.role.image), view = discord.ui.View(ActionButtons.lightsButton, ActionButtons.passButton))

            async def voteCallback(interaction):
                await interaction.response.defer(ephemeral = True)
                message: discord.Message = None
                select = discord.ui.Select(placeholder = "PLAYERS", options = [discord.SelectOption(label = i.name, value = i.id) for i in self.players] + "abstain")
                
                for i in self.players:
                    if i.id == interaction.user.id and i.dead:
                        await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.DEAD.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                        return
                async def selectCallback(interaction):
                    await interaction.response.defer(ephemeral = False)
                    voter: Player = None
                    voted: Player = None

                    for i in self.players:
                        if i.id == interaction.user.id: voter = i
                        if i.id == select.values[0]:    voted = i

                    self.votes[voter.id] = voted.id
                    if all(i.dead or self.votes[i.id] is not None for i in self.players):
                        loser = Counter([i for i in self.votes.values()]).most_common(1)[0]
                        if loser[0] == "abstain": 
                            for i in self.players: self.votes[i.id] = None
                            self.log = f"You breath a sigh of relief. The townspeople have voted to abstain from lynching for the day by {loser[1]} votes."
                            self.round += 1
                            self.save()

                        else:
                            for i in self.players: 
                                self.votes[i.id] = None
                                if i.id == loser[0]: i.dead = True

                                if all(i.dead for i in self.wolves()):
                                    k = 80
                                    avg_winner_sr = sum([User(i.id).sr for i in self.winners])/len([User(i.id).sr for i in self.winners])
                                    avg_loser_sr  = sum([User(i.id).sr for i in self.losers])/len([User(i.id).sr for i in self.losers])

                                    e = 1 / (1 + 10**(avg_winner_sr - avg_loser_sr) / 400)

                                    for i in self.winners:
                                        winner = User(i.id)
                                        winner.stats["bamboozle"]["wins"] += 1
                                        winner.stats["bamboozle"]["sr"] += (k * (1 - e)) * 3 if i in self.wolves() else (k * (1 - e))
                                        
                                        winner.save()
                                    
                                    for i in self.losers:
                                        loser = User(i.id)
                                        loser.stats["bamboozle"]["losses"] += 1
                                        loser.stats["bamboozle"]["sr"] -= (k * (1 - e))
                                        
                                        loser.save()

                                    medalSelect   = discord.ui.Select(placeholder = "Give a player a medal.", row = 1)
                                    endorseSelect = discord.ui.Select(placeholder = "Endorse a player.", row = 2)
                                    claimButton   = discord.ui.Button(emoji = "🎁", label = "CLAIM REWARDS", style = discord.ButtonStyle.green, row = 3)
                                    v = discord.ui.View(medalSelect, endorseSelect, claimButton)

                                    for i in self.players: 
                                        medalSelect.add_option(label = i.name, value = i.name)
                                        endorseSelect.add_option(label = i.name, value = i.name)

                                        pickle.dump(None, open(f"{os.path.join(os.path.dirname(config.__file__), 'data/games')}/{i.id}.p", "wb"))

                                    async def medalCallback(interaction):
                                        await interaction.response.defer(ephemeral = True)
                                        user = None
                                        message = None

                                        if interaction.user.id not in [i.id for i in self.players]: 
                                            await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = "❌ Only people who played in the game can endorse or give medals.", color = config.Color.ERROR))
                                            return
                                        
                                        if interaction.user.name == medalSelect.values[0]:
                                            await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.GENERIC.value, color = config.Color.ERROR), ephemeral = True)
                                            return

                                        for i in self.players:
                                            if i.name == medalSelect.values[0]:
                                                user = User(i.id)
                                                u = User(interaction.user.id)

                                                if i.name in u.medals_given or len(u.medals_given) > u.endorses:
                                                    await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.ALREADY_DID_THAT.value, color = config.Color.ERROR), ephemeral = True)
                                                    return
                                                
                                                u.medals_given.append(i.name)
                                                u.save()

                                        async def callback(interaction):
                                            await interaction.response.defer(ephemeral = True)
                                            match s.values[0]:
                                                case "lucky": user.stats["trust"]["medals"]["lucky"] += 1
                                                case "smart investor": user.stats["trust"]["medals"]["smart investor"] += 1
                                                case "negotiator": user.stats["trust"]["medals"]["negotiator"] += 1
                                                case _: pass
                                            
                                            user.save()
                                            await message.delete()

                                        s = discord.ui.Select(placeholder = "PICK A MEDAL", options = [discord.SelectOption(label = "Lucky", description = "This player always seemed to roll perfectly.", value = "lucky"), discord.SelectOption(label = "Smart Investor", description = "This player knew what to buy and when to upgrade.", value = "smart investor"), discord.SelectOption(label = "Negotiator", description = "They always found clever trades that benefitted them the most.", value = "negotiator")])
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
                                    await interaction.followup.send(embed = discord.Embed(title = f"After {self.round} rounds, the game is over.", description = "- The townspeople won by killing all the wolves!" + ("\n- The **Tanner** also won by getting themselves killed!" if len([i for i in self.players if i.role == Role.TANNER and i.dead]) else "") + ("\n- The **Plague Doctor** also won by giving everyone the plague!" if Role.PLAGUE_DOCTOR in [i.role for i in self.players] and all(i.plague for i in self.players) else "") + ("\n- The **Guardian Angel** also won by helping their Protected survive!" if len([i.role == Role.GAURDIAN_ANGEL and not i.protecting.dead for i in self.players]) > 0 else "") + "\n\nEndorse players or award them medals below.", color = config.Color.COLORLESS), view = discord.ui.View(endorseSelect, medalSelect, claimButton))
                                    return
                                
                                elif all(i.dead for i in self.villagers()):
                                    k = 80
                                    avg_winner_sr = sum([User(i.id).sr for i in self.winners])/len([User(i.id).sr for i in self.winners])
                                    avg_loser_sr  = sum([User(i.id).sr for i in self.losers])/len([User(i.id).sr for i in self.losers])

                                    e = 1 / (1 + 10**(avg_winner_sr - avg_loser_sr) / 400)

                                    for i in self.winners:
                                        winner = User(i.id)
                                        winner.stats["bamboozle"]["wins"] += 1
                                        winner.stats["bamboozle"]["sr"] += (k * (1 - e)) * 3 if i in self.wolves() else (k * (1 - e))
                                        
                                        winner.save()
                                    
                                    for i in self.losers:
                                        loser = User(i.id)
                                        loser.stats["bamboozle"]["losses"] += 1
                                        loser.stats["bamboozle"]["sr"] -= (k * (1 - e))
                                        
                                        loser.save()

                                    medalSelect   = discord.ui.Select(placeholder = "Give a player a medal.", row = 1)
                                    endorseSelect = discord.ui.Select(placeholder = "Endorse a player.", row = 2)
                                    claimButton   = discord.ui.Button(emoji = "🎁", label = "CLAIM REWARDS", style = discord.ButtonStyle.green, row = 3)
                                    v = discord.ui.View(medalSelect, endorseSelect, claimButton)

                                    for i in self.players: 
                                        medalSelect.add_option(label = i.name, value = i.name)
                                        endorseSelect.add_option(label = i.name, value = i.name)

                                        pickle.dump(None, open(f"{os.path.join(os.path.dirname(config.__file__), 'data/games')}/{i.id}.p", "wb"))

                                    async def medalCallback(interaction):
                                        await interaction.response.defer(ephemeral = True)
                                        user = None
                                        message = None

                                        if interaction.user.id not in [i.id for i in self.players]: 
                                            await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = "❌ Only people who played in the game can endorse or give medals.", color = config.Color.ERROR))
                                            return
                                        
                                        if interaction.user.name == medalSelect.values[0]:
                                            await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.GENERIC.value, color = config.Color.ERROR), ephemeral = True)
                                            return

                                        for i in self.players:
                                            if i.name == medalSelect.values[0]:
                                                user = User(i.id)
                                                u = User(interaction.user.id)

                                                if i.name in u.medals_given or len(u.medals_given) > u.endorses:
                                                    await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.ALREADY_DID_THAT.value, color = config.Color.ERROR), ephemeral = True)
                                                    return
                                                
                                                u.medals_given.append(i.name)
                                                u.save()

                                        async def callback(interaction):
                                            await interaction.response.defer(ephemeral = True)
                                            match s.values[0]:
                                                case "lucky": user.stats["trust"]["medals"]["lucky"] += 1
                                                case "smart investor": user.stats["trust"]["medals"]["smart investor"] += 1
                                                case "negotiator": user.stats["trust"]["medals"]["negotiator"] += 1
                                                case _: pass
                                            
                                            user.save()
                                            await message.delete()

                                        s = discord.ui.Select(placeholder = "PICK A MEDAL", options = [discord.SelectOption(label = "Lucky", description = "This player always seemed to roll perfectly.", value = "lucky"), discord.SelectOption(label = "Smart Investor", description = "This player knew what to buy and when to upgrade.", value = "smart investor"), discord.SelectOption(label = "Negotiator", description = "They always found clever trades that benefitted them the most.", value = "negotiator")])
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
                                    await interaction.followup.send(embed = discord.Embed(title = f"After {self.round} rounds, the game is over.", description = "- The wolves won by killing all the townspeople!" + ("\n- The **Tanner** also won by getting themselves killed!" if len([i for i in self.players if i.role == Role.TANNER and i.dead]) else "") + ("\n- The **Plague Doctor** also won by giving everyone the plague!" if Role.PLAGUE_DOCTOR in [i.role for i in self.players] and all(i.plague for i in self.players) else "") + ("\n- The **Guardian Angel** also won by helping their Protected survive!" if len([i.role == Role.GAURDIAN_ANGEL and not i.protecting.dead for i in self.players]) > 0 else "") + "\n\nEndorse players or award them medals below.", color = config.Color.COLORLESS), view = discord.ui.View(endorseSelect, medalSelect, claimButton))
                                    return

                            self.log = f"A hush falls over the town. The townspeople have voted to lynch **<@{loser[0]}>** by {loser[1]} votes."
                            self.round += 1
                            self.save()

                    self.save()

                    e, v = self.render()
                    await message.delete()

                    await self.message.delete()
                    self.message = await interaction.followup.send(embed = e, view = v, ephemeral = False)

                select.callback = selectCallback
                message = await interaction.response.followup.send(embed = discord.Embed(title = "The player with the most votes will die!", color = config.Color.COLORLESS).set_footer(text = config.footer), view = discord.ui.View(select))

            for i in self.players: description += f"\n- **<@{i.id}>**" + (" [DEAD]" if i.dead else " [ALIVE]") + (" [VOTED]" if self.votes[i.id] else " [VOTING]") + (f" ({i.role.title})" if i.dead or i.revealed else "")
            actionButton.callback, voteButton.callback = actionCallback, voteCallback

            return discord.Embed(title = f"BAMBOOZLE! | Day {math.ceil(self.round / 2)}", description = description, color = config.Color.BAMBOOZLE).set_footer(text = config.footer), discord.ui.View(actionButton, voteButton)
    
    class Achievement(Enum):
        # NAME = ("name", "Play 10 games.", "emoji")
        # NAME = {"name", "Play 100 games.", "emoji")
        # NAME = {"name", "Play 1,000 games.", "emoji")
        # NAME = {"name", "Play 100,000 games.", "emoji"

        def __new__(cls, value, description, emoji):
            obj = object.__new__(cls)
            obj._value_ = value

            obj.description = description
            obj.emoji = emoji

            return obj