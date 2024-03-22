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

import random, json, requests
from enum import Enum
from typing import List

name = "The Price is Urban"

description = '''
    Try to guess how many likes and dislikes the given entry has on The Urban Dictionary!\n(powered by The Urban Dictionary)
'''

class Button(discord.ui.Button):
    def __init__(self, game, likes, dislikes):
        super().__init__(style = discord.ButtonStyle.secondary, label = f"{likes}👍 | {dislikes}👎")

        self.game: Game = game
        self.likes: int = likes
        self.dislikes: int = dislikes

        async def callback(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral = False)
            if interaction.user.id != game.user.id: await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.PERMISSION.value, color = config.Color.ERROR).set_footer(text = f"Version: {config.version}"), ephemeral = True)
            
            elif self.likes == game.likes: 
                e, _ = game.render()
                e.color = config.color.SUCCESS
                await game.message.edit(embed = e, view = discord.ui.View())
            
            else: 
                e, _ = game.render()
                e.color = config.Color.ERROR
                await game.message.edit(embed = e, view = discord.ui.View())

        self.callback = callback

class Game():
    def __init__(self, user: User, word: str):
        self.user = user
        self.word = word if word else json.loads(requests.get("https://api.urbandictionary.com/v0/random").text)["list"][0]["word"]
        self.guesses: List[tuple[int]] = []

        self.definition: str = json.loads(requests.get(f"http://api.urbandictionary.com/v0/define?term={self.word}").text)["list"][0]["definition"]
        self.url:        str = json.loads(requests.get(f"http://api.urbandictionary.com/v0/define?term={self.word}").text)["list"][0]["permalink"]
        self.likes:      int = json.loads(requests.get(f"http://api.urbandictionary.com/v0/define?term={self.word}").text)["list"][0]["thumbs_up"]
        self.author:     str = json.loads(requests.get(f"http://api.urbandictionary.com/v0/define?term={self.word}").text)["list"][0]["author"]
        self.example:     str = json.loads(requests.get(f"http://api.urbandictionary.com/v0/define?term={self.word}").text)["list"][0]["example"]
        self.timestamp:  str = json.loads(requests.get(f"http://api.urbandictionary.com/v0/define?term={self.word}").text)["list"][0]["written_on"]
        self.dislikes:   int = json.loads(requests.get(f"http://api.urbandictionary.com/v0/define?term={self.word}").text)["list"][0]["thumbs_down"]

        step_count = random.randint(1, 5)
        like_step_size = round(self.likes / step_count)
        dislike_step_size = round(self.dislikes / step_count)

        for i in range(1, 6): self.guesses.append((i * like_step_size, i * dislike_step_size))


    def render(self) -> tuple[discord.Embed, discord.ui.View]:
        view = discord.ui.View()
        for i in self.guesses: view.add_item(Button(self, i[0], i[1]))
        return discord.Embed(title = self.word, description = self.definition, color = config.Color.COLORLESS, url = self.url, fields = [discord.EmbedField(name = "Example", value = self.example)]).set_footer(text = config.footer).set_author(name = self.author), view

    class Achievement(Enum):
        

        def __new__(cls, value, description, emoji):
            obj = object.__new__(cls)
            obj._value_ = value

            obj.description = description
            obj.emoji = emoji

            return obj