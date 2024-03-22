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

from typing import List
from enum import Enum

name = "Blackjack"

description = '''
    someone remind me to write this
'''

class Suit(Enum):
    HEARTS   = "♥"
    CLUBS    = "♣"
    DIAMONDS = "♦"
    SPADES   = "♠"

class Card():
    def __init__(self, rank: str, suit: Suit):
        self.rank = rank
        self.suit = suit

        try:    self.value = int(rank)
        except: self.value = 11 if rank == "A" else 10

    def __str__(self) -> str:
        return f"{self.rank}{self.suit.value}"

class Game():
    def __init__(self, user, bet):
        if bet > 500: bet = 500
        if bet < 2:   bet = 2

        self.message: discord.Message = None
        self.doubled: bool = False

        self.bet:  int  = bet
        self.user: User = user

        self.deck:   List[Card] = [Card(r, s) for r in ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"] for s in Suit]
        # self.hand:   List[Card] = [self.deck.pop(random.randint(0, len(self.deck) - 1)) for _ in range(2)]
        self.hand:   List[Card] = [Card("9", Suit.CLUBS), Card("7", Suit.CLUBS)]
        self.dealer: List[Card] = [self.deck.pop(random.randint(0, len(self.deck) - 1)) for _ in range(2)]

    def render(self):
        hitButton    = discord.ui.Button(label = "HIT",    style = discord.ButtonStyle.secondary, row = 0)
        standButton  = discord.ui.Button(label = "STAND",  style = discord.ButtonStyle.secondary, row = 0)
        doubleButton = discord.ui.Button(label = "DOUBLE", style = discord.ButtonStyle.secondary, row = 1, disabled = 9 <= sum([i.value for i in self.hand]) >= 11)

        async def hitCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            self.hand.append(self.deck.pop(random.randint(0, len(self.deck))))

            if sum([i.value for i in self.hand]) > 21:
                for i in self.hand: i.value = 1 if i.rank == "A" else i.value
                if sum([i.value for i in self.hand]) > 21: 
                    self.user.stats["blackjack"]["losses"] += 1
                    self.user.chips -= self.bet
                    self.user.save()

                    bust = discord.Embed(title = f"Blackjack! (Bet: {self.bet})", description = f"You BUSTED! Your hand is worth more than 21, and you have lost your **{self.bet}** chip bet. Better luck next time!", color = config.Color.COLORLESS).set_footer(text = config.footer)
                    hand_str:   str = ""
                    dealer_str: str = ""

                    for i in self.hand:   hand_str   += f" `{str(i)}`"
                    for i in self.dealer: dealer_str += f" `{str(i)}`"

                    bust.add_field(name = "Your Hand", value = hand_str, inline = False)
                    bust.add_field(name = "Dealer's Hand", value = dealer_str, inline = False)

                    await self.message.edit(embed = bust, view = discord.ui.View())
                    return
            
            elif True:
                claimButton = discord.ui.Button(emoji = "🎁", label = "CLAIM REWARDS", style = discord.ButtonStyle.green, row = 3)

                self.user.stats["blackjack"]["wins"] += 1
                self.user.chips -= self.bet
                self.user.save()

                won = discord.Embed(title = f"Blackjack! (Bet: {self.bet})", description = f"You WON! You got a **NATURAL BJ** and won your **{self.bet}** chip bet. You should play again!", color = config.Color.COLORLESS).set_footer(text = config.footer)
                hand_str:   str = ""
                dealer_str: str = ""

                for i in self.hand:   hand_str   += f" `{str(i)}`"
                for i in self.dealer: dealer_str += f" `{str(i)}`"

                won.add_field(name = "Your Hand", value = hand_str, inline = False)
                won.add_field(name = "Dealer's Hand", value = dealer_str, inline = False)

                async def claimCallback(interaction):
                    await interaction.response.defer(ephemeral = True)
                    user = User(interaction.user.id)

                    if user.claimed: await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.ALREADY_DID_THAT.value, color = config.Color.ERROR).set_footer(text = f"Version: {config.version}"), ephemeral = True)
                    else:
                        xp, tickets, jackpot = user.award()
                        await interaction.followup.send(embed = discord.Embed(title = "You claimed your Rewards!", description = f"You received **{xp}** experience and **{tickets}** tickets." + (f"\n**JACKPOT!**\nYou also got {jackpot}!" if jackpot else ""), color = config.Color.COLORLESS), ephemeral = True)

                claimButton.callback = claimCallback

                await self.message.edit(embed = won, view = discord.ui.View(claimButton))
                return

            e, v = self.render()
            await self.message.edit(embed = e, view = v)

        async def standCallback(interaction):
            await interaction.response.defer(ephemeral = True)

            while sum([i.value for i in self.dealer]) < 17: self.dealer.append(self.deck.pop(random.randint(0, len(self.deck))))
            if sum([i.value for i in self.dealer]) == 21 or sum([i.value for i in self.hand]) < sum([i.value for i in self.dealer]) <= 21:
                self.user.stats["blackjack"]["losses"] += 1
                self.user.chips -= self.bet
                self.user.save()

                lose = discord.Embed(title = f"Blackjack! (Bet: {self.bet})", description = f"You LOST! The dealer's hand was better than yours. You have lost your **{self.bet}** chip bet. Better luck next time!", color = config.Color.COLORLESS).set_footer(text = config.footer)
                hand_str:   str = ""
                dealer_str: str = ""

                for i in self.hand:   hand_str   += f" `{str(i)}`"
                for i in self.dealer: dealer_str += f" `{str(i)}`"

                lose.add_field(name = "Your Hand", value = hand_str, inline = False)
                lose.add_field(name = "Dealer's Hand", value = dealer_str, inline = False)

                await self.message.edit(embed = lose, view = discord.ui.View())
            
            else:
                self.user.stats["blackjack"]["wins"] += 1
                self.user.chips += self.bet
                self.user.save()

                win = discord.Embed(title = f"Blackjack! (Bet: {self.bet})", description = f"You WON! The dealer's hand was worse than yours. You have won your **{self.bet}** chip bet. You should play again!", color = config.Color.COLORLESS).set_footer(text = config.footer)
                hand_str:   str = ""
                dealer_str: str = ""

                for i in self.hand:   hand_str   += f" `{str(i)}`"
                for i in self.dealer: dealer_str += f" `{str(i)}`"

                win.add_field(name = "Your Hand", value = hand_str, inline = False)
                win.add_field(name = "Dealer's Hand", value = dealer_str, inline = False)

                await self.message.edit(embed = win, view = discord.ui.View())

        async def doubleCallback(interaction):
            await interaction.response.defer(ephemeral = True)

            self.bet *= 2
            self.doubled = True

            e, v = self.render()
            await self.message.edit(embed = e, view = v)

        hitButton.callback, standButton.callback, doubleButton.callback = hitCallback, standCallback, doubleCallback
        embed = discord.Embed(title = f"Blackjack! (Bet: {self.bet})", description = "`HIT` to draw another card. `STAND` to stop drawing. `DOUBLE` to double your bet (if you have 9-11). Get as close to 21 as you can without going over. Aces are 1 or 11; face cards are 10.", color = config.Color.COLORLESS).set_footer(text = config.footer)

        hand_str: str = ""
        for i in self.hand: hand_str += f" `{str(i)}`"

        embed.add_field(name = "Your Hand", value = hand_str, inline = False)
        embed.add_field(name = "Dealer's Hand", value = f"`{str(self.dealer[0])}` `??`", inline = False)

        return embed, discord.ui.View(hitButton, standButton, doubleButton)
    class Achievement(Enum):
        

        def __new__(cls, value, description, emoji):
            obj = object.__new__(cls)
            obj._value_ = value

            obj.description = description
            obj.emoji = emoji

            return obj