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

class chest_14(trust.Card):
    def __init__(self, variant: trust.Variant):
        match variant:
            case trust.Variant.BASE: super().__init__("", "You are assessed for street repair. $40 per house. $115 per hotel", "assets/card.png")
            case trust.Variant.HELLOPOLY: super().__init__("Wirtschaftswunder", "You miraculously recover after the extermination. Collect $40 per house and $115 per hotel.", "assets/card.png")

    def on_draw(self, player, game):
        payout = 0
        for i in player.properties:
            if i.houses < 5:  payout += 40 * i.houses
            if i.houses >= 5: payout += 115

        player.cash += payout
        player.net_worth += payout