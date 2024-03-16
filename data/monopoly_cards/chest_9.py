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

import games.trust as trust

class chest_9(trust.Card):
    def __init__(self):
        super().__init__("Extortion Pays the Bills", "You blackmail your opponents with sundry pictures. Collect $10 from every player.", "assets/card.png")

    def on_draw(self, player, game):
        for i in game.players:
            player.cash += 10
            player.net_worth += 10

            i.cash -= 10
            i.net_worth -= 10