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

class chance_5(trust.Card):
    def __init__(self, variant: trust.Variant):
        match variant:
            case trust.Variant.BASE: super().__init__("", "Advance to the nearest Railroad. Pay double rent if someone else owns it.", "assets/card.png")
            case trust.Variant.HELLOPOLY: super().__init__("GTFO Of Dodge!", "Advance to the nearest Vehicle. Pay double rent if someone else owns it.", "assets/card.png")

    def on_draw(self, player, game):
        vehicles = [5, 15, 25, 34]
        location = game.board[vehicles[min(range(len(vehicles)), key = lambda i: abs(vehicles[i] - player.position))]]
        player.move(game, position = game.board.index(location))

        if location.owner not in [None, player]:
            rent = location.rent[location.owner.vehicles - 1]

            player.cash -= rent
            player.net_worth -= rent

            location.owner.cash += rent
            location.owner.net_worth += rent

