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

class chest_1(trust.Card):
    def __init__(self, variant: trust.Variant):
        match variant:
            case trust.Variant.BASE: super().__init__("Go! Go! Go!", "Advance to Go. Collect $200", "assets/card.png")
            case trust.Variant.HELLOPOLY: super().__init__("Go! Go! Go!", "Advance to Go. Collect $200", "assets/card.png")

    def on_draw(self, player, game):
        player.move(game, position = 0)