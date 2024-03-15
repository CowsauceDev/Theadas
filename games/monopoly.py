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

from typing import List
import config
from theadas import User

import discord
import random, importlib, os, io, copy, pickle

from enum import Enum
from PIL import Image

description = '''
    someone remind me to write this
'''

class Variant(Enum):
    BASE = "Base Set"

class Card():
    def __init__(self, name, description, image):
        self.name = name
        self.description = description
        self.image = image
    
    def __str__(self):
        return f"{self.name}"
    
    def on_draw(self, player, game):
        return
    
    @classmethod
    def load(self, name):
        if os.path.exists(f"data/monopoly_cards/{name}.py"):
            spec = importlib.util.spec_from_file_location(name, f"data/monopoly_cards/{name}.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

        return getattr(module, name)
    
class Set(Enum):
    BROWN = "Envy"
    LIGHT_BLUE = "Sloth"
    PURPLE = "Gluttony"
    ORANGE = "Lust"
    RED = "Greed"
    YELLOW = "Wrath"
    GREEN = "Pride"
    DARK_BLUE = "Heaven"

    RAILROADS = "Vehicles"
    PORTALS  = "Portals"
    SPECIAL  = ""

    discord.Message.edit

class Location():
    def __init__(self, name, image, cost, rent, mortgage, set, coords):
        self.name = name
        self.image = image
        self.cost = cost
        self.rent = rent
        self.mortgage = mortgage
        self.set = set
        self.coords = coords

        self.houses = 0
        self.owner = None
        self.mortgaged = False

class Player:
    def __init__(self, id, name):
        self.id: int = id
        self.name: str = name

        self.free: bool = True
        self.piece = None
        self.position: int = 0

        self.cash: int = 1500
        self.net_worth: int = 1500
        self.has_card: bool = False

        self.properties: List[Location] = []
        self.vehicles: int = 0
        self.portals: int = 0

    def move(self, game, spaces = None, position = None):
        if spaces: 
            try: self.position = (self.position + spaces) % len(game.board)
            except: pass

        if position: self.position = position
        location = game.board[self.position]

        if location.owner and not location.mortgaged:
            if location.set == Set.RAILROADS: rent = location.rent[location.owner.vehicles]
            elif location.set == Set.PORTALS: rent = location.rent[location.owner.portals]
            else: rent = location.rent[location.houses]

            self.cash      -= rent
            self.net_worth -= rent

            location.owner.cash      += rent
            location.owner.net_worth += rent

            if location.owner != self: game.log(f"{self.name} pays {location.owner.name} ${rent} in rent.")

        # go
        if self.position == 0:
            self.cash      += 200
            self.net_worth += 200
            game.log(f"{self.name} collects $200.")
        
        # income tax
        if self.position == 4:
            self.cash      -= 200
            self.net_worth -= 200
            game.log(f"{self.name} pays $200.")

        # luxury tax
        if self.position == 38:
            self.cash      -= 100
            self.net_worth -= 100
            game.log(f"{self.name} pays $100.")

        # go to jail
        if self.position == 30:
            self.position = 10
            self.free = False
        
        # chest
        if self.position in [2, 17, 33]:
            chest = [i for i in os.listdir("data/monopoly_cards") if i.startswith("chest")]
            card = Card.load(random.choice(chest).split(".")[0])()
            card.on_draw(game.active, game)
            game.card = card

        # chance
        if self.position in [7, 22, 35]:
            chance = [i for i in os.listdir("data/monopoly_cards") if i.startswith("chance")]
            card = Card.load(random.choice(chance).split(".")[0])()
            card.on_draw(game.active, game)
            game.card = card
        
        game.save()

    class Piece(Enum):
        THIMBLE = ("Thimble", "assets/thimble.png")
        TOPHAT = ("Top Hat", "assets/tophat.png")
        IRON = ("Iron", "assets/iron.png")
        CAT = ("Cat", "assets/cat.png")
        WHEELBARROW = ("Wheelbarrow", "assets/wheelbarrow.png")
        TERRIER = ("Scottish Terrier", "assets/scottish_terrier.png")
        RACECAR = ("Racecar", "assets/racecar.png")
        BATTLESHIP = ("Battleship", "assets/battleship.png")

        def __new__(cls, value, image):
            obj = object.__new__(cls)
            obj._value_ = value

            obj.title = value
            obj.image = image

            return obj

class Game():
    def __init__(self, players):
        self.players: List[Player] = players
        self.losers:  List[Player] = []
        self.message: discord.Message = None
        self.active: Player = random.choice(players)

        self.rolled:   bool = False
        self.can_roll: bool = True

        self._log: List[str] = ["The game was started!"]
        self.card: Card = None
        self.board: List[Location] = [
            Location("Go", "", None, None, None, Set.SPECIAL, (40, 40)), # 0
            Location("Mediterranian Avenue", "", 60, [4, 10, 3, 90, 160, 250], 30, Set.BROWN, (134, 40)), # 1
            Location("Community Chest", "", None, None, None, Set.SPECIAL, (208, 40)), # 2
            Location("Baltic Avenue", "", 60, [8, 20, 60, 180, 320, 450], 30, Set.BROWN, (282, 40)), # 3
            Location("Income Tax", "", None, None, None, Set.SPECIAL, (356, 40)), # 4
            Location("Reading Railroad", "", 200, [25, 50, 100, 200], 100, Set.RAILROADS, (356, 40)), # 5
            Location("Oriental Avenue", "", 100, [12, 30, 90, 270, 400, 550], 50, Set.LIGHT_BLUE, (504, 40)), # 6
            Location("Chance", "", None, None, None, Set.SPECIAL, (578, 40)), # 7
            Location("Vermont Avenue", "", 100, [12, 30, 90, 270, 400, 550], 50, Set.LIGHT_BLUE, (652, 40)), # 8
            Location("Connecticut Avenue", "", 120, [16, 40, 100, 300, 450, 600], 60, Set.LIGHT_BLUE, (726, 40)), # 9
            Location("Jail", "", None, None, None, Set.SPECIAL, (848, 11)), # 10
            Location("St. Charles Place", "", 140, [20, 50, 150, 450, 625, 750], 70, Set.PURPLE, (820, 134)), # 11
            Location("Electric Company", "", 150, [4, 10], 60, Set.PORTALS, (820, 208)), # 12
            Location("States Avenue", "", 140, [20, 50, 150, 450, 625, 750], 70, Set.PURPLE, (820, 282)), # 13
            Location("Virginia Avenue", "", 160, [24, 60, 180, 500, 700, 900], 80, Set.PURPLE, (820, 356)), # 14
            Location("Pennsylvania Railroad", "", 200, [25, 50, 100, 200], 30, Set.RAILROADS, (820, 430)), # 15
            Location("St. James Place", "", 180, [14, 28, 70, 200, 550, 750, 950], 90, Set.ORANGE, (820, 504)), # 16
            Location("Community Chest", "", None, None, None, Set.SPECIAL, (820, 578)), # 17
            Location("Tennesse Avenue", "", 180, [14, 28, 70, 200, 550, 750, 950], 90, Set.ORANGE, (820, 652)), # 18
            Location("New York Avenue", "", 200, [32, 80, 220, 600, 800, 1000], 100, Set.ORANGE, (820, 726)), # 19
            Location("Free Parking", "", None, None, None, Set.SPECIAL, (820, 820)), # 20
            Location("Kentucky Avenue", "", 220, [40, 90, 250, 700, 850, 1050], 86, Set.RED, (726, 820)), # 21
            Location("Chance", "", None, None, None, Set.SPECIAL, (652, 820)), # 22
            Location("Indiana Avenue", "", 220, [40, 90, 250, 700, 850, 1050], 86, Set.RED, (578, 820)), # 23
            Location("Illinois Avenue", "", 240, [40, 100, 300, 750, 925, 860], 120, Set.RED, (504, 820)), # 24
            Location("B&O Railroad", "", 200, [25, 50, 100, 200], 30, Set.RAILROADS, (430, 820)), # 25
            Location("Atlantic Avenue", "", 260, [44, 86, 330, 800, 975, 1150], 130, Set.YELLOW, (356, 820)), # 26
            Location("Ventnor Avenue", "", 260, [44, 86, 330, 800, 975, 1150], 130, Set.YELLOW, (282, 820)), # 27
            Location("Water Works", "", 150, [4, 10], 60, Set.PORTALS, (208, 820)), # 28
            Location("Marvin Gardens", "", 280, [48, 120, 400, 850, 1025, 1200], 140, Set.YELLOW, (134, 820)), # 29
            Location("Go to Jail!", "", None, None, None, Set.SPECIAL, (40, 820)), # 30
            Location("Pacific Avenue", "", 300, [52, 130, 390, 900, 860, 1275], 150, Set.GREEN, (40, 726)), # 31
            Location("North Carolina Avenue", "", 300, [52, 130, 390, 900, 860, 1275], 150, Set.GREEN, (40, 652)), # 32
            Location("Community Chest", "", None, None, None, Set.SPECIAL, (40, 578)), #33
            Location("Pennsylvania Avenue", "", 320, [56, 150, 450, 1000, 1200, 1400], 160, Set.GREEN, (40, 504)), # 34
            Location("Chance", "", None, None, None, Set.SPECIAL, (40, 430)), # 35
            Location("I.M.P Van", "", 200, [25, 50, 100, 200], 30, Set.RAILROADS, (430, 40)), # 36
            Location("Park Place", "", 350, [70, 175, 500, 860, 1300, 1500], 175, Set.DARK_BLUE, (40, 282)), # 37
            Location("Luxury Tax", "", None, None, None, Set.SPECIAL, (40, 208)), # 38
            Location("Boardwalk", "", 400, [100, 200, 600, 1400, 1700, 2000], 200, Set.DARK_BLUE, (40, 134)) # 39
        ]

        for i in self.players:
            user = User(i.id)
            user.medals_given = []
            user.endorses_given = []
            user.claimed = False

            user.save()
        self.save()
    
    def save(self):
        game = copy.copy(self)
        game.message = None
        game.card = None

        for i in self.players: pickle.dump(game, open(f"{os.path.join(os.getcwd(), 'data/games')}/{i.id}.p", "wb"))

    def log(self, message):
        if len(self._log) < 3: self._log.append(message)
        else:
            self._log[0] = self._log[1]
            self._log[1] = self._log[2]
            self._log[2] = message

        self.save()

    def render(self):
        embed = discord.Embed()
        view = discord.ui.View(timeout = None)

        embed.title = f"**It is {self.active.name}'s turn.**"
        embed.description = ""
        embed.color = config.Color.HELLARED
        embed.set_footer(text = config.footer)
        embed.set_image(url = "attachment://board.png")

        board = Image.open("assets/board.png").resize((894, 894))
        bytes = io.BytesIO()
        positions = []
        
        # if self.card: board.paste(Image.open(self.card.image).resize((274, 438)), (310, 228))
        for i in self.players:
            if i.piece:
                coords = self.board[i.position].coords if i.free else (791, 68)
                for p in positions: 
                    if p == i.position: coords = (coords[0] - 3, coords[1] - 6)

                piece = Image.open(i.piece.image).resize((34, 34))
                board.paste(piece, coords, piece)
                positions.append(i.position)

        board.save(bytes, "png")
        bytes.seek(0)

        # embed.image = "" TODO: render board

        for i in self.players: 
            properties = "Properties:"
            for p  in i.properties: properties += f"\n{p.name}" + (" (mortgaged)" if p.mortgaged else "")
            embed.add_field(name = i.name, value = f"Net Worth: {i.net_worth}\nCash: {i.cash}\nProperties: {len(i.properties)}" + (f" **[[Hover]]({self.message.jump_url} \"{properties}\")**" if self.message and len(i.properties) > 0 else ""), inline = True)
        for i in self._log: embed.description += f"{i}\n"

        rollButton     = discord.ui.Button(style = discord.ButtonStyle.secondary, emoji = "🎲", label = "ROLL", disabled = not self.can_roll)
        tradeButton    = discord.ui.Button(style = discord.ButtonStyle.secondary, emoji = "🤝", label = "TRADE")
        buyButton      = discord.ui.Button(style = discord.ButtonStyle.secondary, emoji = "🛒", label = "BUY PROPERTY")
        auctionButton  = discord.ui.Button(style = discord.ButtonStyle.secondary, emoji = "🎤", label = "AUCTION PROPERTY")
        mortgageButton = discord.ui.Button(style = discord.ButtonStyle.secondary, emoji = "📜", label = "MORTGAGE")
        houseButton    = discord.ui.Button(style = discord.ButtonStyle.secondary, emoji = "⬆️", label = "BUY HOUSES")
        sellButton     = discord.ui.Button(style = discord.ButtonStyle.secondary, emoji = "⬇️", label = "SELL HOUSES")
        endButton      = discord.ui.Button(style = discord.ButtonStyle.secondary, emoji = "❌", label = "END TURN")
        bailButton     = discord.ui.Button(style = discord.ButtonStyle.secondary, emoji = "⛓️", label = "POST BAIL")
        outButton      = discord.ui.Button(style = discord.ButtonStyle.secondary, emoji = "🗝️", label = "GET OUT OF HORNY_JAIL FREE")
        pieceButton    = discord.ui.Button(style = discord.ButtonStyle.secondary, emoji = "♟️", label = "CHOOSE A PIECE")
        bankruptButton = discord.ui.Button(style = discord.ButtonStyle.secondary, emoji = "🏳️", label = "BANKRUPT")

        async def rollCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user.id == self.active.id:
                player: Player = None
                for i in self.players: 
                    if i.id == interaction.user.id: player = i

                roll = [random.randint(1, 6), random.randint(1, 6)]
                spaces = roll[0] + roll[1]
                location = self.board[(self.active.position + spaces) % len(self.board)]

                if self.active.free or roll[0] == roll[1]: 
                    self.log(f"{self.active.name} rolls `{roll[0]}, {roll[1]}` and moves to `{location.name}`" + (" (just visiting)" if location == self.board[10] else ""))
                    player.move(self, spaces = spaces)
                else: self.log(f"{self.active.name} rolls `{roll[0]}, {roll[1]}`")

                self.can_roll = roll[0] == roll[1]
                self.rolled = True
                self.save()

                e, v, f = self.render()
                await self.message.edit(embed = e, view = v, file = f, attachments = [])

            else: 
                e = discord.Embed()
                e.title = random.choice(config.error_titles)
                e.color = config.Color.ERROR
                e.description = config.Error.WRONG_TURN.value
                e.set_footer(text = config.footer)

                await interaction.followup.send(embed = e, ephemeral = True)

        async def tradeCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            v = discord.ui.View()
            e = discord.Embed()

            player1 = None
            message = None

            offer  = []
            demand = []

            players = discord.ui.Select(placeholder = "PLAYER TO TRADE WITH")

            for i in self.players:
                if i.id == interaction.user.id: player1 = i
                else: players.add_option(label = i.name, value = i.name)

            e.title = "Trading..."
            e.color = config.Color.HELLARED
            e.description = f"**Sent by:** {player1.name}\n**Sent to:** None"
            e.add_field(name = "Offer:", value = "Nothing offered")
            e.add_field(name = "Demand:", value = "Nothing demanded")
            e.set_footer(text = config.footer)

            async def playersCallback(interaction):
                await interaction.response.defer(ephemeral = True)
                player2 = None

                for i in self.players:
                    if players.values[0] == i.name: player2 = i

                offer1 = discord.ui.Select(placeholder = "OFFER A PROPERTY")
                offer2 = discord.ui.Select(placeholder = "OFFER A PROPERTY")

                demand1 = discord.ui.Select(placeholder = "DEMAND A PROPERTY")
                demand2 = discord.ui.Select(placeholder = "DEMAND A PROPERTY")

                confirmButton = discord.ui.Button(style = discord.ButtonStyle.secondary, emoji = "✅", label = "CONFIRM", disabled = True)

                for i in player1.properties:
                    if len(offer1.options) < 14: offer1.add_option(label = i.name, value = i.name)
                    else: offer2.add_option(label = i.name, value = i.name)

                for i in player2.properties:
                    if len(offer1.options) < 14: demand1.add_option(label = i.name, value = i.name)
                    else: demand2.add_option(label = i.name, value = i.name)

                async def offerCallback(interaction):
                    await interaction.response.defer(ephemeral = True)

                    if offer1.values[0]:
                        for i in player1.properties:
                            if i.title == offer1.values[0] and i not in offer: offer.append(i)

                    elif offer2.values[0]:
                        for i in player1.properties:
                            if i.title == offer1.values[0] and i not in offer: offer.append(i)

                    s = ""
                    for i in offer: s += i.title

                    e.clear_fields()
                    e.add_field(name = "Offer:", value = s)
                    e.add_field(name = "Demand:", value = "Nothing demanded")

                    confirmButton.disabled = False
                    await message.edit(embed = e, view = v)

                async def demandCallback(interaction):
                    await interaction.response.defer(ephemeral = True)

                    if demand1.values[0]:
                        for i in player2.properties:
                            if i.title == demand1.values[0] and i not in offer: demand.append(i)

                    elif demand2.values[0]:
                        for i in player2.properties:
                            if i.title == demand2.values[0] and i not in offer: demand.append(i)

                    s1 = ""
                    for i in offer: s1 += i.title

                    s2 = ""
                    for i in demand: s2 += i.title

                    e.clear_fields()
                    e.add_field(name = "Offer:", value = s1)
                    e.add_field(name = "Demand:", value = s2)

                    v = discord.ui.View()
                    confirmButton.disabled = False

                    v.add_item(demand1)
                    v.add_item(confirmButton)

                    if len(demand2.options) > 0: v.add_item(demand2)
                    await message.edit(embed = e, view = v)

                async def confirmCallback(interaction):
                    try: await interaction.response.defer()
                    except: pass

                    if len(demand) == 0:
                        confirmButton.disabled = True
                        v = discord.ui.View()

                        v.add_item(demand1)
                        v.add_item(confirmButton)

                        if len(demand2.options) > 0: v.add_item(demand2)
                        await message.edit(embed = e, view = v)
                    
                    else:                                                        
                        await message.delete()

                        m = None
                        v = discord.ui.View()

                        acceptButton = discord.ui.Button(style = discord.ButtonStyle.success,label = "ACCEPT OFFER")
                        rejectButton  = discord.ui.Button(style = discord.ButtonStyle.danger, label = "REJECT OFFER")

                        async def acceptCallback(interaction):
                            await interaction.response.defer()
                            if interaction.user.id == player2.id:
                                await m.delete()
                                self.log(f"{player2.name} accepted a trade from {player1.name}.")

                                for i in offer: player1.properties.remove(i)
                                for i in offer: player2.properties.append(i)

                                for i in demand: player2.properties.remove(i)
                                for i in demand: player1.properties.append(i)

                                self.save()
                                e, v, f = self.render()
                                await self.message.edit(embed = e, view = v, file = f, attachments = [])
                            
                            else:
                                e = discord.Embed()
                                e.title = random.choice(config.error_titles)
                                e.color = config.Color.ERROR
                                e.description = config.Error.WRONG_TURN.value
                                e.set_footer(text = config.footer)

                                await interaction.followup.send(embed = e, ephemeral = True)

                        async def rejectCallback(interaction):
                            await interaction.response.defer()
                            if interaction.user.id == player2.id:
                                await m.delete()
                                self.log(f"{player2.name} rejected a trade from {player1.name}.")
                                self.save()

                                e, v, f = self.render()
                                await self.message.edit(embed = e, view = v, file = f, attachments = [])
                            
                            else:
                                e = discord.Embed()
                                e.title = random.choice(config.error_titles)
                                e.color = config.Color.ERROR
                                e.description = config.Error.WRONG_TURN.value
                                e.set_footer(text = config.footer)

                                await interaction.followup.send(embed = e, ephemeral = True)

                        acceptButton.callback = acceptCallback
                        rejectButton.callback = rejectCallback

                        v.add_item(acceptButton)
                        v.add_item(rejectButton)

                        m = await interaction.followup.send(embed = e, view = v)
                                
                offer1.callback = offerCallback
                offer2.callback = offerCallback

                demand1.callback = demandCallback
                demand2.callback = demandCallback

                confirmButton.callback = confirmCallback

                v.remove_item(players)
                v.add_item(offer1)
                v.add_item(confirmButton)
                e.description = f"**Sent by:** {player1.name}\n**Sent to:** {player2.name}"
                if len(offer2.options) > 0: v.add_item(offer2)

                await message.edit(embed = e, view = v)

            players.callback = playersCallback
            v.add_item(players)
            message = await interaction.followup.send(embed = e, view = v, ephemeral = True)

        async def buyCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user.id == self.active.id:
                location = self.board[self.active.position]
                location.owner = self.active

                self.log(f"{self.active.name} has purchased {location.name} for ${location.cost}.")
                self.active.cash -= location.cost
                self.active.properties.append(location)
                self.save()
                
                e, v, f = self.render()
                await self.message.edit(embed = e, view = v, file = f, attachments = [])

            else: 
                e = discord.Embed()
                e.title = random.choice(config.error_titles)
                e.color = config.Color.ERROR
                e.description = config.Error.WRONG_TURN.value
                e.set_footer(text = config.footer)

                await interaction.followup.send(embed = e, ephemeral = True)

        async def auctionCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user.id == self.active.id:
                e = discord.Embed()
                e.title = random.choice(config.error_titles)
                e.color = config.Color.ERROR
                e.description = "Auctions are not yet implemented."
                e.set_footer(text = config.footer)

                await interaction.followup.send(embed = e, ephemeral = True)

            else: 
                e = discord.Embed()
                e.title = random.choice(config.error_titles)
                e.color = config.Color.ERROR
                e.description = config.Error.WRONG_TURN.value
                e.set_footer(text = config.footer)

                await interaction.followup.send(embed = e, ephemeral = True)

        async def mortgageCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            message = None
            v = discord.ui.View()

            s1 = discord.ui.Select(placeholder = "CHOOSE A PROPERTY TO MORTGAGE")
            s2 = discord.ui.Select(placeholder = "CHOOSE A PROPERTY TO MORTGAGE")

            for i in self.active.properties:
                if len(s1.options) < 14: s1.add_option(label = i.title, value = i.title)
                else: s2.add_option(label = i.title, value = i.title)

            async def selectCallback(interaction):
                await interaction.response.defer(ephemeral = True)

                location = None

                if s1.values[0]:
                    for i in self.active.properties:
                        if i.title == s1.values[0]:
                            location = i
                            i.mortgaged = True

                            self.active.cash += i.mortgage
                            self.active.net_worth += i.mortgage

                elif s2.values[0]:
                    for i in self.active.properties:
                        if i.title == s1.values[0]:
                            location = i
                            i.mortgaged = True

                            self.active.cash += i.mortgage
                            self.active.net_worth += i.mortgage

                await message.delete()
                self.log(f"{self.active.name} has mortgaged {location.name} for ${location.mortgage}.")
                self.save()

                e, v, f = self.render()
                await self.message.edit(embed = e, view = v, file = f, attachments = [])
                            
            s1.callback = selectCallback
            s2.callback = selectCallback

            v.add_item(s1)
            if len(s2.options) > 0: v.add_item(s2)
            
            message = await interaction.followup.send(view = v, ephemeral = True)

        async def houseCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            message = None
            v = discord.ui.View()

            s1 = discord.ui.Select(placeholder = "PICK A PROPERTY")
            s2 = discord.ui.Select(placeholder = "PICK A PROPERTY")

            for i in self.active.properties:
                if len(s1.options) < 14: s1.add_option(label = i.title, value = i.title)
                else: s2.add_option(label = i.title, value = i.title)

            async def selectCallback(interaction):
                await interaction.response.defer(ephemeral = True)

                location = None
                even     = True
                monopoly = True

                if interaction.user.id != self.active.id:
                    e = discord.Embed()
                    e.title = random.choice(config.error_titles)
                    e.color = config.Color.ERROR
                    e.description = config.Error.WRONG_TURN.value
                    e.set_footer(text = config.footer)

                    await interaction.followup.send(embed = e, ephemeral = True)
                    return
                
                if s1.values[0]:
                    for i in self.active.properties:
                        if i.title == s1.values[0]: location = i

                    for i in self.board:
                        if i.set == location.set and i.owner != self.active: monopoly = False
                        if i.set == location.set and i.houses < location.houses: even = False

                    if even and monopoly and self.active.cash >= location.cost:
                        location.houses += 1
                        self.active.cash -= location.cost
                        self.log(f"{self.active.name} has bought a house on {location.name} for ${location.cost}.")
                        self.save()

                    elif self.active.cash >= location.cost:
                        e = discord.Embed()
                        e.title = random.choice(config.error_titles)
                        e.color = config.Color.ERROR
                        e.description = ("" if monopoly else "You must own every property in a set to build houses.") + ("" if even else "You must build houses and hotels evenly.")
                        e.set_footer(text = config.footer)

                        await interaction.followup.send(embed = e, ephemeral = True)
                    
                    else:
                        e = discord.Embed()
                        e.title = random.choice(config.error_titles)
                        e.color = config.Color.ERROR
                        e.description = config.Error.INSUFFICIENT_FUNDS.value
                        e.set_footer(text = config.footer)

                        await interaction.followup.send(embed = e, ephemeral = True)

                elif s2.values[0]:
                    for i in self.active.properties:
                        if i.title == s1.values[0]: location = i

                    for i in self.board:
                        if i.set == location.set and i.owner != self.active: monopoly = False
                        if i.set == location.set and i.houses < location.houses: even = False

                    if even and monopoly:
                        location.houses += 1
                        self.active.cash -= location.cost
                        self.log(f"{self.active.name} has bought a house on {location.name} for ${location.cost}.")
                        self.save()

                    else:
                        e = discord.Embed()
                        e.title = random.choice(config.error_titles)
                        e.color = config.Color.ERROR
                        e.description = ("" if monopoly else "You must own every property in a set to build houses.") + ("" if even else "You must build houses and hotels evenly.")
                        e.set_footer(text = config.footer)

                        await interaction.followup.send(embed = e, ephemeral = True)

                await message.delete()
                e, v, f = self.render()
                await self.message.edit(embed = e, view = v, file = f, attachments = [])
                            
            s1.callback = selectCallback
            s2.callback = selectCallback

            v.add_item(s1)
            if len(s2.options) > 0: v.add_item(s2)
            message = await interaction.followup.send(view = v, ephemeral = True)

        async def sellCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            message = None
            v = discord.ui.View()

            s1 = discord.ui.Select("PICK A PROPERTY")
            s2 = discord.ui.Select("PICK A PROPERTY")

            for i in self.active.properties:
                if len(s1.options) < 14 and i.houses > 0: s1.add_option(label = i.title, value = i.title)
                elif i.houses > 0: s2.add_option(label = i.title, value = i.title)

            async def selectCallback(interaction):
                await interaction.response.defer(ephemeral = True)

                location = None
                even     = True

                if interaction.user.id != self.active.id:
                    e = discord.Embed()
                    e.title = random.choice(config.error_titles)
                    e.color = config.Color.ERROR
                    e.description = config.Error.WRONG_TURN.value
                    e.set_footer(text = config.footer)

                    await interaction.followup.send(embed = e, ephemeral = True)
                    return

                if s1.values[0]:
                    for i in self.active.properties:
                        if i.title == s1.values[0]: location = i

                    for i in self.board:
                        if i.set == location.set and i.houses > location.houses: even = False

                    if even:
                        location.houses -= 1
                        self.active.cash += location.cost
                        self.log(f"{self.active.name} has sold a house on {location.name} for ${location.cost}.")
                        self.save()

                    else:
                        e = discord.Embed()
                        e.title = random.choice(config.error_titles)
                        e.color = config.Color.ERROR
                        e.description = "You must build houses and hotels evenly."
                        e.set_footer(text = config.footer)

                        await interaction.followup.send(embed = e, ephemeral = True)

                elif s2.values[0]:
                    for i in self.active.properties:
                        if i.title == s1.values[0]: location = i

                    for i in self.board:
                        if i.set == location.set and i.owner != self.active: monopoly = False
                        if i.set == location.set and i.houses < location.houses: even = False

                    if even:
                        location.houses -= 1
                        self.active.cash += location.cost
                        self.log(f"{self.active.name} has sold a house on {location.name} for ${location.cost}.")
                        self.save()

                    else:
                        e = discord.Embed()
                        e.title = random.choice(config.error_titles)
                        e.color = config.Color.ERROR
                        e.description = "You must build houses and hotels evenly."
                        e.set_footer(text = config.footer)

                        await interaction.followup.send(embed = e, ephemeral = True)

                await message.delete()
                e, v, f = self.render()
                await self.message.edit(embed = e, view = v, file = f, attachments = [])
                            
            s1.callback = selectCallback
            s2.callback = selectCallback

            v.add_item(s1)
            if len(s2.options) > 0: v.add_item(s2)
            
            message = await interaction.followup.send(view = v, ephemeral = True)

        async def endCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user.id == self.active.id:
                index = self.players.index(self.active)

                self.active = self.players[index + 1 if index < len(self.players) - 1 else 0]
                self.rolled = False
                self.can_roll = True
                
                self.save()
                e, v, f = self.render()
                await self.message.edit(embed = e, view = v, file = f, attachments = [])

            else: 
                e = discord.Embed()
                e.title = random.choice(config.error_titles)
                e.color = config.Color.ERROR
                e.description = config.Error.WRONG_TURN.value
                e.set_footer(text = config.footer)

                await interaction.followup.send(embed = e, ephemeral = True)

        async def bankruptCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user.id == self.active.id:
                index = self.players.index(self.active)
                for i in self.active.properties: i.owner = None

                u = User(self.active.id)
                u.stats["monopoly"]["losses"] += 1
                u.save()

                self.players.remove(self.active)
                self.losers .append(self.active)

                self.active = self.players[index + 1 if index < len(self.players) - 1 else 0]
                self.rolled = False
                self.can_roll = True
                self.save()

                if len(self.players) == 1:
                    winner = User(self.players[0].id)
                    winner.stats["monopoly"]["wins"] += 1
                    winner.save()

                    medalSelect   = discord.ui.Select(placeholder = "Give a player a medal.", row = 1)
                    endorseSelect = discord.ui.Select(placeholder = "Endorse a player.", row = 2)
                    claimButton   = discord.ui.Button(emoji = "🎁", label = "CLAIM REWARDS", style = discord.ButtonStyle.green, row = 3)
                    v = discord.ui.View(medalSelect, endorseSelect, claimButton)

                    for i in self.players + self.losers: 
                        medalSelect.add_option(label = i.name, value = i.name)
                        endorseSelect.add_option(label = i.name, value = i.name)

                        pickle.dump(None, open(f"{os.path.join(os.getcwd(), 'data/games')}/{i.id}.p", "wb"))

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
                                case "lucky": user.stats["monopoly"]["medals"]["lucky"] += 1
                                case "smart investor": user.stats["monopoly"]["medals"]["smart investor"] += 1
                                case "negotiator": user.stats["monopoly"]["medals"]["negotiator"] += 1
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

                    _, _, f = self.render()
                    await self.message.edit(embed = discord.Embed(title = f"{self.players[0].name} wins!", description = "Endorse players or award them medals below.", color = config.Color.COLORLESS), view = v, file = f, attachments = [])

                else:
                    e, v, f = self.render()
                    await self.message.edit(embed = e, view = v, file = f, attachments = [])

            else: 
                e = discord.Embed()
                e.title = random.choice(config.error_titles)
                e.color = config.Color.ERROR
                e.description = config.Error.WRONG_TURN.value
                e.set_footer(text = config.footer)

                await interaction.followup.send(embed = e, ephemeral = True)

        async def bailCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user.id == self.active.id:
                self.active.cash -= 50
                self.active.net_worth -= 50
                self.active.free = True
                self.can_roll = False

                self.log(f"{self.active.name} posts $50 as bail.")
                self.save()

                e, v, f = self.render()
                await self.message.edit(embed = e, view = v, file = f, attachments = [])

            else: 
                e = discord.Embed()
                e.title = random.choice(config.error_titles)
                e.color = config.Color.ERROR
                e.description = config.Error.WRONG_TURN.value
                e.set_footer(text = config.footer)

                await interaction.followup.send(embed = e, ephemeral = True)

        async def outCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user.id == self.active.id:
                self.active.has_card = False
                self.active.free = True
                self.can_roll = False

                self.log(f"{self.active.name} used their Get Out of Jail Free card.")
                self.save()

                e, v, f = self.render()
                await self.message.edit(embed = e, view = v, file = f, attachments = [])

            else: 
                e = discord.Embed()
                e.title = random.choice(config.error_titles)
                e.color = config.Color.ERROR
                e.description = config.Error.WRONG_TURN.value
                e.set_footer(text = config.footer)

                await interaction.followup.send(embed = e, ephemeral = True)
        
        async def pieceCallback(interaction):
            await interaction.response.defer(ephemeral = True)

            player = None
            message = None

            for i in self.players: 
                if i.id == interaction.user.id: player = i
            
            if player.id == self.active.id:
                select = discord.ui.Select(placeholder = f"PICK YOUR PIECE")
                v = discord.ui.View(timeout = None)

                for i in Player.Piece: 
                    if i not in [i.piece for i in self.players]: select.add_option(label = i.value, value = i.value)

                async def selectCallback(interaction):
                    await interaction.response.defer(ephemeral = True)
                    match select.values[0]:
                        case Player.Piece.THIMBLE.value:     player.piece = Player.Piece.THIMBLE
                        case Player.Piece.TOPHAT.value:      player.piece = Player.Piece.TOPHAT
                        case Player.Piece.IRON.value:        player.piece = Player.Piece.IRON
                        case Player.Piece.CAT.value:         player.piece = Player.Piece.CAT
                        case Player.Piece.WHEELBARROW.value: player.piece = Player.Piece.WHEELBARROW
                        case Player.Piece.TERRIER.value:     player.piece = Player.Piece.TERRIER
                        case Player.Piece.RACECAR.value:     player.piece = Player.Piece.RACECAR
                        case Player.Piece.BATTLESHIP.value:  player.piece = Player.Piece.BATTLESHIP
                        case _: return

                    await message.delete()
                    self.log(f"{self.active.name} is playing as `{self.active.piece.value}`")
                    self.save()

                    e, v, f = self.render()
                    await self.message.edit(embed = e, view = v, file = f, attachments = [])
                                
                select.callback = selectCallback
                v.add_item(select)
                
                message = await interaction.followup.send(view = v, ephemeral = True)

            else:
                e = discord.Embed()
                e.title = random.choice(config.error_titles)
                e.description = config.Error.WRONG_TURN.value
                e.color = config.Color.ERROR
                e.set_footer(text = config.footer)

                await interaction.followup.send(embed = e, ephemeral = True)

        rollButton.callback     = rollCallback
        tradeButton.callback    = tradeCallback
        buyButton.callback      = buyCallback
        auctionButton.callback  = auctionCallback
        mortgageButton.callback = mortgageCallback
        houseButton.callback    = houseCallback
        sellButton.callback     = sellCallback
        endButton.callback      = endCallback
        bailButton.callback     = bailCallback
        outButton.callback      = outCallback
        pieceButton.callback    = pieceCallback
        bankruptButton.callback = bankruptCallback

        if self.active.piece:
            if self.rolled:
                location = self.board[self.active.position]
                if location.owner == None and location.cost:
                    if self.active.cash >= location.cost: view.add_item(buyButton)
                    view.add_item(auctionButton)

            if not self.can_roll and self.active.cash >= 0: view.add_item(endButton)

            elif not self.active.free: 
                if self.active.has_card: view.add_item(outButton)
                if self.active.cash >= 50: view.add_item(bailButton)

            view.add_item(rollButton)
            view.add_item(mortgageButton)
            view.add_item(houseButton)
            view.add_item(sellButton)
            view.add_item(tradeButton)
            view.add_item(bankruptButton)
        
        else: view.add_item(pieceButton)


        return embed, view, discord.File(fp = bytes, filename = "board.png")

    class Achievement(Enum):
        

        def __new__(cls, value, description, emoji):
            obj = object.__new__(cls)
            obj._value_ = value

            obj.description = description
            obj.emoji = emoji

            return obj
        


# hellopoly board
        
# self.board: List[Location] = [
# Location("Go", "", None, None, None, Set.SPECIAL, (40, 40)), # 0
# Location("Mediterranian Avenue", "", 60, [4, 10, 3, 90, 160, 250], 30, Set.BROWN, (134, 40)), # 1
# Location("Community Chest", "", None, None, None, Set.SPECIAL, (208, 40)), # 2
# Location("NV", "", 60, [8, 20, 60, 180, 320, 450], 30, Set.BROWN, (282, 40)), # 3
# Location("Income Tax", "", None, None, None, Set.SPECIAL, (356, 40)), # 4
# Location("Crimson's Helicopter", "", 200, [25, 50, 100, 200], 100, Set.RAILROADS, (356, 40)), # 5
# Location("St. An Hospital", "", 100, [12, 30, 90, 270, 400, 550], 50, Set.LIGHT_BLUE, (504, 40)), # 6
# Location("Chance", "", None, None, None, Set.SPECIAL, (578, 40)), # 7
# Location("Rehab", "", 100, [12, 30, 90, 270, 400, 550], 50, Set.LIGHT_BLUE, (652, 40)), # 8
# Location("Belphegor's Pharmacy", "", 120, [16, 40, 100, 300, 450, 600], 60, Set.LIGHT_BLUE, (726, 40)), # 9
# Location("Horny Jail", "", None, None, None, Set.SPECIAL, (848, 11)), # 10
# Location("Bee's Eats", "", 140, [20, 50, 150, 450, 625, 750], 70, Set.PURPLE, (820, 134)), # 11
# Location("Stolas' Grimoire", "", 150, [4, 10], 60, Set.PORTALS, (820, 208)), # 12
# Location("Beezelehaven", "", 140, [20, 50, 150, 450, 625, 750], 70, Set.PURPLE, (820, 282)), # 13
# Location("Beelzebub's Mansion", "", 160, [24, 60, 180, 500, 700, 900], 80, Set.PURPLE, (820, 356)), # 14
# Location("Verosika Mayday's Car", "", 200, [25, 50, 100, 200], 30, Set.RAILROADS, (820, 430)), # 15
# Location("Ozzie's", "", 180, [14, 28, 70, 200, 550, 750, 950], 90, Set.ORANGE, (820, 504)), # 16
# Location("Community Chest", "", None, None, None, Set.SPECIAL, (820, 578)), # 17
# Location("Asmodeus' Factory", "", 180, [14, 28, 70, 200, 550, 750, 950], 90, Set.ORANGE, (820, 652)), # 18
# Location("Asmodeus Tower", "", 200, [32, 80, 220, 600, 800, 1000], 100, Set.ORANGE, (820, 726)), # 19
# Location("Free Parking", "", None, None, None, Set.SPECIAL, (820, 820)), # 20
# Location("LooLoo Land", "", 220, [40, 90, 250, 700, 850, 1050], 86, Set.RED, (726, 820)), # 21
# Location("Chance", "", None, None, None, Set.SPECIAL, (652, 820)), # 22
# Location("Crimson's Manor", "", 220, [40, 90, 250, 700, 850, 1050], 86, Set.RED, (578, 820)), # 23
# Location("Mammon Theater", "", 240, [40, 100, 300, 750, 925, 860], 120, Set.RED, (504, 820)), # 24
# Location("The 666 Elevator", "", 200, [25, 50, 100, 200], 30, Set.RAILROADS, (430, 820)), # 25
# Location("Rough N' Tumbeleweed Ranch", "", 260, [44, 86, 330, 800, 975, 1150], 130, Set.YELLOW, (356, 820)), # 26
# Location("Hideaway Motel", "", 260, [44, 86, 330, 800, 975, 1150], 130, Set.YELLOW, (282, 820)), # 27
# Location("Asmodean Crystal", "", 150, [4, 10], 60, Set.PORTALS, (208, 820)), # 28
# Location("Stryker's Mineshaft", "", 280, [48, 120, 400, 850, 1025, 1200], 140, Set.YELLOW, (134, 820)), # 29
# Location("Go to Jail!", "", None, None, None, Set.SPECIAL, (40, 820)), # 30
# Location("I.M.P Headquarters", "", 300, [52, 130, 390, 900, 860, 1275], 150, Set.GREEN, (40, 726)), # 31
# Location("Cannibal Town", "", 300, [52, 130, 390, 900, 860, 1275], 150, Set.GREEN, (40, 652)), # 32
# Location("Community Chest", "", None, None, None, Set.SPECIAL, (40, 578)), #33
# Location("The Hazbin Hotel", "", 320, [56, 150, 450, 1000, 1200, 1400], 160, Set.GREEN, (40, 504)), # 34
# Location("Chance", "", None, None, None, Set.SPECIAL, (40, 430)), # 35
# Location("I.M.P Van", "", 200, [25, 50, 100, 200], 30, Set.RAILROADS, (430, 40)), # 36
# Location("Cherub Town", "", 350, [70, 175, 500, 860, 1300, 1500], 175, Set.DARK_BLUE, (40, 282)), # 37
# Location("Luxury Tax", "", None, None, None, Set.SPECIAL, (40, 208)), # 38
# Location("The Courtroom", "", 400, [100, 200, 600, 1400, 1700, 2000], 200, Set.DARK_BLUE, (40, 134)) # 39
# ]