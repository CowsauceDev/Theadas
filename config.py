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

from enum import Enum

version = "0.1"
token = ""
owner = 645064200502378506

footer = f"/credits | Version: {version}"

error_titles = [
    "Oh no!",
]

credits = {
    "**[@cowsauce](https://discord.gg/pZ9r5jm2)**": "bot owner, developer, artist, tester",
    "**@alicane**": "server owner, designer, tester",
    "**[@gooeygumi](https://discord.gg/Z2ZnZFZQ)**": "artist",
    "**Rinnegan**": "tester",
}

class Error(Enum):
    GENERIC = "❌ Something went wrong."
    PERMISSION = "❌ You do not have permission to use that command."
    NOT_IMPLEMENTED = "❌ This game has not been implemented yet."
    IN_GAME = "❌ You are already in a game!"
    NOT_IN_GAME = "❌ You are already in a game!"
    ALREADY_DID_THAT = "❌ You already did that."
    WRONG_TURN = "❌ Wait until your turn to do that."
    NOT_ENOUGH = "❌ You do not have enough for that!"

    # WOB
    CZAR = "❌ You cannot play a card while you are the Czar."
    NOT_CZAR = "❌ Only the Czar can choose a winning card."
    
class Color():
    COLORLESS = 0x2b2d31
    ERROR     = 0xED4245
    SUCCESS   = 0x40A45F

    # WOB
    BLACK_CARD = 0x000000
    WHITE_CARD = 0xFFFFFF

    # Monopoly
    HELLARED  = 0xEE2051