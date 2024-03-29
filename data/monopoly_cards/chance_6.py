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

import games.trust as trust

class chance_6(trust.Card):
    def __init__(self, variant: trust.Variant):
        match variant:
            case trust.Variant.BASE: super().__init__("", "Advance to the nearest Utility.", "assets/card.png")
            case trust.Variant.HELLOPOLY: super().__init__("Trip to the Human World!", "Advance to the nearest Portal.", "assets/card.png")

    def on_draw(self, player, game):
        portals = [14, 28]
        location = game.board[portals[min(range(len(portals)), key = lambda i: abs(portals[i] - player.position))]]
        player.move(game, position = location)

