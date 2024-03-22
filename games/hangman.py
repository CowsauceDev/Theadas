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
from wonderwords import RandomWord

name = "Hangman"

description = '''
    Guess letters until you reveal the whole word.\nIf you guess wrong too many times, you will be hanged!
'''

letters: List[str] = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
gallows: dict = {
    6: '''
```   ____
|    |
|
|
|
|
_|_
|   |______
|          |
|__________|
```
    ''',

    5: '''
```   ____
|    |
|    o
|
|
|
_|_
|   |______
|          |
|__________|
```
    ''',

    4: '''
```   ____
|    |
|    o
|    |
|    |
|
_|_
|   |______
|          |
|__________|
```
    ''',

    3: '''
```   ____
|    |
|    o
|   /|
|    |
|
_|_
|   |______
|          |
|__________|
```
    ''',

    2: '''
```   ____
|    |
|    o
|   /|\\
|    |
|
_|_
|   |______
|          |
|__________|
```
    ''',

    1: '''
```   ____
|    |
|    o
|   /|\\
|    |
|   /
_|_
|   |______
|          |
|__________|
```
    ''',

    0: '''
```   ____
|    |
|    o
|   /|\\
|    |
|   / \\
_|_
|   |______
|          |
|__________|
```
    '''
}

class Game():
    def __init__(self, user):
        self.message: discord.Message = None
        self.user: User = user

        self.word: str = RandomWord().word(word_min_length = 5, word_max_length = 7)
        self.guesses: List[str] = [random.choice(letters)]
        self.lives = 6

        self.user.plays["hangman"] -= 1
        self.user.save()

    def render(self):
        select: discord.ui.Select = discord.ui.Select(placeholder = "GUESS A LETTER")

        for i in letters:
            if i not in self.guesses: select.add_option(label = i, value = i)

        async def selectCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            won = True

            self.guesses.append(select.values[0])
            if select.values[0] not in self.word: self.lives -= 1

            for i in self.word:
                if i != " " and i not in self.guesses: won = False

            if self.lives <= 0: 
                self.user.stats["hangman"]["losses"] += 1
                self.user.save()

                lost = discord.Embed(title = f"Hangman ({len(self.word)} letters)", description = f"You LOST! You made too many wrong guesses and got hanged!\n{gallows[self.lives]}", color = config.Color.COLORLESS).set_footer(text = config.footer)
                guesses_str: str = ""

                for i in self.guesses: guesses_str += ("**" if i in self.word else "") + f"{i}" + ("**, " if i in self.word else ", ")

                lost.add_field(name = "Word", value = self.word, inline = False)
                lost.add_field(name = "Guesses", value = guesses_str[:-2], inline = False)

                await self.message.edit(embed = lost, view = discord.ui.View())
            
            elif won:
                self.user.stats["hangman"]["wins"] += 1
                self.user.save()

                won = discord.Embed(title = f"Hangman ({len(self.word)} letters)", description = f"You WON! You guessed every letter in the word before getting hanged!\n{gallows[self.lives]}", color = config.Color.COLORLESS).set_footer(text = config.footer)
                guesses_str: str = ""

                for i in self.guesses: guesses_str += ("**" if i in self.word else "") + f"{i}" + ("**, " if i in self.word else ", ")

                won.add_field(name = "Word", value = self.word, inline = False)
                won.add_field(name = "Guesses", value = guesses_str[:-2], inline = False)

                await self.message.edit(embed = won, view = discord.ui.View())

            else:
                e, v = self.render()
                await self.message.edit(embed = e, view = v)

        select.callback = selectCallback
        embed = discord.Embed(title = f"Hangman ({len(self.word)} letters)", description = f"Guess letters until you reveal the whole word. If you guess wrong too many times, you will be hanged! Your random free guess was **{self.guesses[0]}.**\n{gallows[self.lives]}", color = config.Color.COLORLESS).set_footer(text = config.footer)

        word_str = ""
        guesses_str = ""

        for i in self.word: word_str += i if i in self.guesses or i == " " else "\_"
        for i in self.guesses: guesses_str += ("**" if i in self.word else "") + f"{i}" + ("**, " if i in self.word else ", ")

        embed.add_field(name = "Word:", value = word_str, inline = False)
        embed.add_field(name = "Guesses:", value = guesses_str[:-2], inline = False)

        return embed, discord.ui.View(select)
    class Achievement(Enum):
        

        def __new__(cls, value, description, emoji):
            obj = object.__new__(cls)
            obj._value_ = value

            obj.description = description
            obj.emoji = emoji

            return obj