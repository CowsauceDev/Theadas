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

class chance_14(trust.Card):
    def __init__(self, variant: trust.Variant):
        match variant:
            case trust.Variant.BASE: super().__init__("", "You have been elected Chairman of the Board. Pay each player $50.", "assets/card.png")
            case trust.Variant.HELLOPOLY: super().__init__("Is That a Bribe?!", "You bribe each player with $50.", "assets/card.png")

    def on_draw(self, player, game):
        for i in game.players:
            player.cash -= 50
            player.net_worth -= 50

            i.cash += 50
            i.net_worth += 50