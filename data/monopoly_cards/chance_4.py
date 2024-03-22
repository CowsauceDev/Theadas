# Theadas Bot is a Discord bot allowing users to play various games with each other.
# Copyright © 2024 Jester (@cowsauce)

# This file is part of Theadas Bot.

# Theadas Bot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Theadas Bot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty ofs
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import games.trust as trust

class chance_4(trust.Card):
    def __init__(self, variant: trust.Variant):
        match variant:
            case trust.Variant.BASE: super().__init__("", "Advance to St. Charles Place. Collect $200 if you pass go.", "assets/card.png")
            case trust.Variant.HELLOPOLY: super().__init__("You Need Somebody Gone", "Advance to I.M.P Headquarters. Collect $200 if you pass go.", "assets/card.png")

    def on_draw(self, player, game):
        if player.position > 31:
            player.cash += 200
            player.net_worth += 200
        player.move(game, position = 31)