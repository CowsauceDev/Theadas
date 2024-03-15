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

import games.bamboozle as bamboozle, games.gridlock as gridlock, games.whiteonblack as whiteonblack, games.monopoly as monopoly

from enum import Enum
from datetime import datetime
from typing import List

import os, pickle, math

# TODO: figure this out

class User:
    def __init__(self, id):
        self.id = id

        if os.path.exists(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p"):
            user: User = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb"))

            self.join: float = user.join
            self.subscribed_since: float = user.subscribed_since
            self.priority_until:   float = user.priority_until
            self.medals_per_game:  int   = user.medals_per_game

            self.titles:       List[str] = user.titles
            self.backgrounds:  List[str] = user.backgrounds
            self.turing:       List[str] = user.turing
            self.guides:       List[str] = user.guides
            self.card_holos:   List[gridlock.Game.Card | bamboozle.Game.Role] = user.card_holos

            self.expansions: List[whiteonblack.Expansion] = user.expansions
            self.variants: List[monopoly.Variant] = user.variants

            self.tickets: int = user.tickets
            self.tokens:  int = user.tokens

            self.chips: int = user.chips
            self.xp: int = user. xp
            self.endorsements: int = user.endorsements

            self.dice: int = user.dice
            self.dominoes: int = user.dominoes
            self.tiles: int = user.tiles
            self.chits: int = user.chits

            self.sr: dict = user.sr
            self.plays: dict = user.plays
            self.packs: dict = user.packs
            self.achievements: dict = user.achievements
            self.stats: dict = user.stats

        else:
            self.join: float = math.floor(datetime.now().timestamp())
            self.subscribed_since: float = None
            self.priority_until:   float = None
            self.medals_per_game: int = 1

            self.titles:      List[str] = ["Novice"]
            self.backgrounds: List[str] = ["assets/default_background.png"]
            self.turing:      List[str] = ["whiteonblack"]
            self.guides:      List[str] = ["2048", "checkers"]
            self.card_holos:  List[gridlock.Game.Card | bamboozle.Game.Role]  = []

            self.expansions:  List[whiteonblack.Expansion] = [whiteonblack.Expansion.BASE]
            self.variants:  List[monopoly.Expansion] = [monopoly.Variant.BASE]

            self.tickets: int = 200
            self.tokens:  int = 0

            self.chips: int = 500
            self.xp: int = 0
            self.endorsements: int = 0

            self.dice: int = 0 # consumables, 456 🎟️ or 142 🪙
            self.dominoes: int = 0 # variants, 325 🪙
            self.tiles: int = 0 # cosmetics, 245 🎟️ or 76 🪙
            self.chits: int = 0 # qol, 648 🪙

            '''
            chips for gambling

            tcg packs
            one week of matchmaking priority
            puzzle plays
            
            whiteonblack packs
            monopoly variants

            profile backgrounds
            holo arts for the tcg and bamboozle role cards

            ai in chess, checkers, monopoly, bamboozle (ai always available in whiteonblack, )
            strategy guides for all the strategy games
            endorse 2 people / game





            subscription service gives access to all whiteonblack packs and monopoly variants, matchmaking priority, and n tokens / month
            '''

            self.sr = {
                "bamboozle": 100,
                "checkers": 100,
                "chess": 100,
                "gridlock": 100
            }

            self.plays = {
                "2048": 1,
                "hangman": 1
            }

            self.packs = {
                gridlock.Pack.SMALL: 0,
                gridlock.Pack.LARGE: 1,
                gridlock.Pack.PREMIUM: 0
            }

            self.achievements = {
                "theadas": [],
                "bamboozle": [],
                "blackjack": [],
                "whiteonblack": [],
                "checkers": [],
                "chess": [],
                "gridlock": [],
                "hangman": [],
                "holdem": [],
                "rps": [],
                "slots": [],
                "tictactoe": [],
                "2048": []
            }

            self.stats = {
                "bamboozle": {
                    "wins": 0,
                    "losses": 0,

                    "medals": {
                        "manipulator": 0,
                        "poker face": 0,
                        "backstabber": 0
                    }
                },

                "blackjack": {
                    "wins": 0,
                    "losses": 0,
                },

                "whiteonblack": {
                    "games": 0,

                    "medals": {
                        "lucky": 0,
                        "funny": 0,
                        "nasty": 0,
                        "offensive": 0
                    }
                },

                "checkers": {
                    "wins": 0,
                    "losses": 0,

                    "medals": {
                        "played well": 0
                    }
                },

                "chess": {
                    "wins": 0,
                    "losses": 0,

                    "medals": {
                        "knowledgable": 0,
                        "risk taker": 0,
                        "played fast": 0
                    }
                },

                "gridlock": {
                    "wins": 0,
                    "losses": 0,

                    "medals": {
                        "interesting deck": 0,
                        "played well": 0,
                        "played fast": 0,
                    }
                },

                "hangman": {
                    "wins": 0,
                    "losses": 0
                },

                "holdem": {
                    "wins": 0,
                    "losses": 0,

                    "medals": {
                        "high roller": 0,
                        "bluff master": 0
                    }
                },

                "monopoly": {
                    "wins": 0,
                    "losses": 0,

                    "medals": {
                        "lucky": 0,
                        "smart investor": 0,
                        "negotiator": 0
                    }
                },

                "rps": {
                    "wins": 0,
                    "losses": 0,
                },

                "slots": {
                    "wins": 0,
                    "losses": 0,
                },
                "tictactoe": {
                    "wins": 0,
                    "losses": 0,
                },
                "2048": {
                    "games": 0
                }
            }

            self.save()
    
    def save(self): pickle.dump(self, open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{self.id}.p", "wb"))
    def get_level(self): return int(0.08 * math.sqrt(self.xp))
    def get_next_level(self): return int(((self.get_level() + 1) / 0.08)) ** 2

    def achievement_str(self, game):
        str = ""
        column = 1

        for i in self.achievements[game]:
            if self.achievements[game].index(i) >= 100: break
            if column < 10: 
                str += i.emoji 
                column += 1
            
            else:
                str += f"\n{i.emoji}"
                column = 1

        return str