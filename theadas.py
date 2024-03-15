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

import config 

import discord
from discord.ext.pages import Page, Paginator, PaginatorButton

import math, random, os, pickle
from enum     import Enum
from datetime import datetime
from typing   import List

if __name__ == "__main__":
    import games.bamboozle        as bamboozle
    import games.blackjack        as blackjack
    import games.whiteonblack     as whiteonblack
    import games.checkers         as checkers
    import games.chess            as chess
    import games.gridlock         as gridlock
    import games.hangman          as hangman
    import games.holdem           as holdem
    import games.monopoly         as monopoly
    import games.rps              as rps
    import games.slots            as slots
    import games.tictactoe        as tictactoe
    import games.twentyfortyeight as twentyfortyeight

class Achievement(Enum):
    EAGER = ("Eager", "Play every game once.", "🏆")
    CONTRIBUTOR = ("Contributor", "Contribute to the bot's developement.", "🏆")
    SUBSCRIBER = ("Subscriber", "Purchase a premium subscription.", "🏆")

    def __new__(cls, value, description, emoji):
        obj = object.__new__(cls)
        obj._value_ = value

        obj.description = description
        obj.emoji = emoji

        return obj

class User:
    def __init__(self, id, guild = None):
        self.id = id

        if os.path.exists(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p"):
            user: User = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb"))

            self.join: float = user.join
            self.subscribed_since: float = user.subscribed_since
            self.priority_until:   float = user.priority_until

            self.endorses: int = user.endorses
            self.medals_given: List[str] = user.medals_given
            self.endorses_given: List[str] = user.endorses_given
            self.claimed: bool = user.claimed

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

            self.endorses: int = 1
            self.medals_given: List[str] = 0
            self.endorses_given: List[str] = 0
            self.claimed: bool = False

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
                "2048": 3,
                "hangman": 3
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
                "monopoly": [],
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
                    "games": 0,
                    "high_score": 0
                }
            }

            pickle.dump(None, open(f"{os.path.join(os.path.dirname(__file__), 'data/games')}/{self.id}.p", "wb"))
            self.save()

            if guild:
                guild.users.append(self.id)
                guild.save()
    
    def save(self): pickle.dump(self, open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{self.id}.p", "wb"))
    def get_level(self): return int(0.08 * math.sqrt(self.xp))
    def get_next_level(self): return int(((self.get_level() + 1) / 0.08)) ** 2

    def game(self): 
        try: return pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/games')}/{self.id}.p", "rb"))
        except: return None

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

        return str if len(str) > 0 else "None"
    
    def award(self, win: bool = False):
        xp = int(random.randint(25, 55)  * (1.2 if win else 1))
        tickets = int(random.randint(28, 68)  * (1.2 if win else 1))
        jackpot = None

        self.tickets += tickets
        self.xp += xp

        if int(random.randint(1, 100) / (1.2 if win else 1)) <= 10:
            match random.randint(1, 6):
                case 1:
                    t = random.randint(228, 268)
                    self.tickets += t
                    jackpot = f"**{t}** extra tickets"
                case 2: 
                    self.dice += 1
                    jackpot = "a free **dice**"
                case 3: 
                    game = random.choice(self.game().keys())
                    self.plays[game] += 1
                    jackpot = "a free play for **{game}**"
                case 4: 
                    c = random.randint(50, 300)
                    self.tickets += c
                    jackpot = f"**{c}** free chips"
                case 5: 
                    self.tokens += 10
                    jackpot = "**10** free Tokens"
                case 6: 
                    self.packs[gridlock.Pack.SMALL] += 1
                    jackpot = "a free **Small Pack** for Gridlock"
        
        self.claimed = True
        self.save()
        return xp, tickets, jackpot

class Guild:
    def __init__(self, id):
        self.id = id
        if os.path.exists(f"{os.path.join(os.path.dirname(__file__), 'data/guilds')}/{id}.p"):
            guild: Guild = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/guilds')}/{id}.p", "rb"))
            self.users = guild.users
            self.sharing: bool = guild.sharing
        else:
            self.users = []
            self.sharing: bool = False

            self.save()

    def save(self): pickle.dump(self, open(f"{os.path.join(os.path.dirname(__file__), 'data/guilds')}/{self.id}.p", "wb"))

bot = discord.Bot(activity = discord.Game("Play games with friends!"))

@bot.event
async def on_ready():
    await bot.register_commands(delete_existing = True)

info = bot.create_group("info", "See information about this game!")
play = bot.create_group("play", "Play a game!")
help = bot.create_group("help", "Learn how to use any command.")

@bot.slash_command(name = "ping", description = "Test the bot's latency.")
async def pingCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)
    embed = discord.Embed(title = "Pong!", description = f"The bot's latency is currently {round(bot.latency, 2)}ms.").set_footer(text = config.footer)

    if bot.latency > 30: embed.color = discord.Color.red()
    else: embed.color = discord.Color.green()

    await ctx.interaction.followup.send(embed = embed)

# pyright: reportInvalidTypeForm=false
@bot.slash_command(name = "profile", description = "View a user's profile.")
async def profileCommand(ctx, user: discord.Option(discord.Member, "Leave blank to check your own.") = None, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)
    if user is None: user = ctx.author
    u: User = User(user.id, Guild(ctx.guild.id))

    moreSelect = discord.ui.Select(placeholder = "See More...", options = [
        discord.SelectOption(label = "Titles", value = "titles"),
        discord.SelectOption(label = "Backgrounds", value = "backgrounds"),
        discord.SelectOption(label = "Holo Cards", value = "holos"),
        discord.SelectOption(label = "CAH Packs", value = "whiteonblack"),
        discord.SelectOption(label = "monopoly Variants", value = "monopoly"),
        discord.SelectOption(label = "Achievements", value = "achievements"),
        discord.SelectOption(label = "Medals", value = "medals")
    ])

    changeSelect = discord.ui.Select(placeholder = "Change Your...")
    if len(u.titles) > 1: changeSelect.add_option(label = "Title", value = "title")
    if len(u.backgrounds) > 1: changeSelect.add_option(label = "Profile Background", value = "background")

    async def moreCallback(interaction):
        await interaction.response.defer(ephemeral = True)

        match moreSelect.values[0]:
            case "titles": pass
            case "backgrounds": pass
            case "holos": pass
            case "whiteonblack": pass
            case "monopoly": pass
            case _: pass

    async def changeCallback(interaction):
        await interaction.response.defer(ephemeral = True)
        
        match changeSelect.values[0]:
            case "title": pass
            case "background": pass
            case _: pass

    moreSelect.callback   = moreCallback
    changeSelect.callback = changeCallback

    view = discord.ui.View(moreSelect)
    if user == ctx.author and len(changeSelect.options) > 0: view.add_item(changeSelect)

    xp_str = ""
    titles_str = ""
    guides_str = ""
    variant_str = ""
    expansion_str = ""
    gridlock_holos = 0
    bamboozle_holos = 0

    for i in range(10): xp_str += "▰" if i < round((u.xp / u.get_next_level()) * 10) else "▱"
    for i in u.variants: variant_str += f"{i.value}, "
    for i in u.expansions: expansion_str += f"{i.value}, "
    for i in u.card_holos: gridlock_holos += 1 if type(i) == gridlock.Game.Card else 0
    for i in u.card_holos: bamboozle_holos += 1 if type(i) == bamboozle.Game.Role else 0

    for i in u.titles:  
        if u.titles.index(i) <= 4: titles_str += f", \"{i}\""
        else:
            titles_str += f", and **{len(u.titles) - u.titles.index(i)}** more"
            break
    
    for i in u.guides:  
        if u.guides.index(i) <= 4: guides_str += f", {i}"
        else:
            guides_str += f", and **{len(u.guides) - u.guides.index(i)}** more"
            break

    if len(variant_str) > 0: variant_str = variant_str[:-2]
    else: variant_str = "None"

    if len(expansion_str) > 0: expansion_str = expansion_str[:-2]
    else: expansion_str = "None"

    embed = discord.Embed(title = user.name + (" ⭐" if u.subscribed_since else " ") + f" (player since <t:{u.join}:D>)", description = f"**Tickets:** {u.tickets}\n**Tokens:** {u.tokens}\n**Chips:** {u.chips}\n\n**Dice:** {u.dice}\n**Dominoes:** {u.dominoes}\n**Tiles:** {u.tiles}\n**Chits:** {u.chits}\n\n**Endorsements:** {u.endorsements}\n**Level:** {u.get_level()} | **XP:** {u.xp} `{xp_str}`\n**Turing Progress:** {len(u.turing)} / 6\n\n**Achievements:** {u.achievement_str('theadas')}", color = config.Color.COLORLESS).set_footer(text = config.footer)
    if u.stats["2048"]["games"] > 0: embed.add_field(name = '2048',  value = f"Games Played: {u.stats['2048']['games']}\n\nAchievements: {u.achievement_str('2048')}", inline = False)
    if u.stats["bamboozle"]["wins"] + u.stats["bamboozle"]["losses"] > 0: embed.add_field(name = "BAMBOOZLE!", value = f"Skill Rating (SR): {math.floor(u.sr['bamboozle'])}\nGames Played: {u.stats['bamboozle']['wins'] + u.stats['bamboozle']['losses']}\nGames Won: {u.stats['bamboozle']['wins']} ({math.floor(u.stats['bamboozle']['wins'] / (u.stats['bamboozle']['wins'] + u.stats['bamboozle']['losses'])) * 100})% Winrate\nHolo Cards Owned: {bamboozle_holos}\n\nAchievements: {u.achievement_str('bamboozle')}\nMedals: ```Manipulator: {u.stats['bamboozle']['medals']['manipulator']}\nPoker Face: {u.stats['bamboozle']['medals']['poker face']}\nBackstabber: {u.stats['bamboozle']['medals']['backstabber']}```", inline = False)
    if u.stats["blackjack"]["wins"] + u.stats["blackjack"]["losses"] > 0: embed.add_field(name = "Blackjack",  value = f"Games Played: {u.stats['blackjack']['wins'] + u.stats['blackjack']['losses']}\n\nAchievements: {u.achievement_str('blackjack')}", inline = False)
    if u.stats["whiteonblack"]["games"] > 0: embed.add_field(name = "White on Black",  value = f"Games Played: {u.stats['whiteonblack']['games']}\n\nExpansions Owned: {expansion_str}\nAchievements: {u.achievement_str('whiteonblack')}\nMedals: ```Lucky: {u.stats['whiteonblack']['medals']['lucky']}\nFunny: {u.stats['whiteonblack']['medals']['funny']}\nNasty: {u.stats['whiteonblack']['medals']['nasty']}\nOffensive: {u.stats['whiteonblack']['medals']['offensive']}```", inline = False)
    if u.stats["checkers"]["wins"] + u.stats["checkers"]["losses"] > 0: embed.add_field(name = "Checkers",  value = f"Skill Rating (SR): {math.floor(u.sr['checkers'])}\nGames Played: {u.stats['checkers']['wins'] + u.stats['checkers']['losses']}\nGames Won: {u.stats['checkers']['wins']} ({math.floor(u.stats['checkers']['wins'] / (u.stats['checkers']['wins'] + u.stats['checkers']['losses'])) * 100})% Winrate\n\nAchievements: {u.achievement_str('checkers')}\nMedals: ```Played Well: {u.stats['checkers']['medals']['played well']}```", inline = False)
    if u.stats["chess"]["wins"] + u.stats["chess"]["losses"] > 0: embed.add_field(name = "Chess",  value = f"Skill Rating (SR): {math.floor(u.sr['chess'])}\nGames Played: {u.stats['chess']['wins'] + u.stats['chess']['losses']}\nGames Won: {u.stats['chess']['wins']} ({math.floor(u.stats['chess']['wins'] / (u.stats['chess']['wins'] + u.stats['chess']['losses'])) * 100})% Winrate\n\nAchievements: {u.achievement_str('chess')}\nMedals: ```Knowledgeable: {u.stats['chess']['medals']['knowledgeable']}\nRisk Taker: {u.stats['chess']['medals']['risk taker']}\nPlayed fast: {u.stats['chess']['medals']['played Fast']}```", inline = False)
    if u.stats["gridlock"]["wins"] + u.stats["gridlock"]["losses"] > 0: embed.add_field(name = "Gridlock",  value = f"Skill Rating (SR): {math.floor(u.sr['gridlock'])}\nGames Played: {u.stats['gridlock']['wins'] + u.stats['gridlock']['losses']}\nGames Won: {u.stats['gridlock']['wins']} ({math.floor(u.stats['gridlock']['wins'] / (u.stats['gridlock']['wins'] + u.stats['gridlock']['losses'])) * 100})% Winrate\nHolo Cards Owned: {gridlock_holos}\n**Packs:** {u.packs[gridlock.Pack.SMALL]} Small, {u.packs[gridlock.Pack.LARGE]} Large, {u.packs[gridlock.Pack.PREMIUM]} Premium\n\nAchievements: {u.achievement_str('gridlock')}\nMedals: ```Interesting Deck: {u.stats['gridlock']['medals']['interesting deck']}\nPlayed Well: {u.stats['gridlock']['medals']['played well']}\nPlayed Fast: {u.stats['gridlock']['medals']['played fast']}```", inline = False)
    if u.stats["hangman"]["wins"] + u.stats["hangman"]["losses"] > 0: embed.add_field(name = "Hangman",  value = f"Games Played: {u.stats['hangman']['wins'] + u.stats['hangman']['losses']}\n\nGames Won: {u.stats['hangman']['wins']} ({math.floor(u.stats['hangman']['wins'] / (u.stats['hangman']['wins'] + u.stats['hangman']['losses'])) * 100})% Winrate\n\nAchievements: {u.achievement_str('hangman')}", inline = False)
    if u.stats["monopoly"]["wins"] + u.stats["monopoly"]["losses"] > 0: embed.add_field(name = "monopoly",  value = f"Games Played: {u.stats['monopoly']['wins'] + u.stats['monopoly']['losses']}\nGames Won: {u.stats['monopoly']['wins']} ({math.floor(u.stats['monopoly']['wins'] / (u.stats['monopoly']['wins'] + u.stats['monopoly']['losses'])) * 100})% Winrate\n\nVariants Owned: {variant_str}\nAchievements: {u.achievement_str('monopoly')}\nMedals: ```Lucky: {u.stats['monopoly']['medals']['lucky']}\nSmart Investor: {u.stats['monopoly']['medals']['smart investor']}\nNegotiator: {u.stats['monopoly']['medals']['negotiator']}```", inline = False)
    if u.stats["rps"]["wins"] + u.stats["rps"]["losses"] > 0: embed.add_field(name = "Rock Paper Scissors",  value = f"Games Played: {u.stats['rps']['wins'] + u.stats['rps']['losses']}\n\nGames Won: {u.stats['rps']['wins']} ({math.floor(u.stats['rps']['wins'] / (u.stats['rps']['wins'] + u.stats['rps']['losses'])) * 100})% Winrate\n\nAchievements: {u.achievement_str('rps')}", inline = False)
    if u.stats["slots"]["wins"] + u.stats["slots"]["losses"] > 0: embed.add_field(name = "Blackjack",  value = f"Games Played: {u.stats['slots']['wins'] + u.stats['slots']['losses']}\n\nAchievements: {u.achievement_str('slots')}", inline = False)
    if u.stats["tictactoe"]["wins"] + u.stats["tictactoe"]["losses"] > 0: embed.add_field(name = "Tic Tac Toe",  value = f"Games Played: {u.stats['tictactoe']['wins'] + u.stats['tictactoe']['losses']}\n\nGames Won: {u.stats['tictactoe']['wins']} ({math.floor(u.stats['tictactoe']['wins'] / (u.stats['tictactoe']['wins'] + u.stats['tictactoe']['losses'])) * 100})% Winrate\n\nAchievements: {u.achievement_str('tictactoe')}", inline = False)

    await ctx.interaction.followup.send(embed = embed, view = view)

@bot.slash_command(name = "shop", description = "Turn your currency into shiny new toys!")
async def shopCommand(ctx):
    await ctx.defer(ephemeral = True)
    user = User(ctx.author.id)

    ticketsSelect = discord.ui.Select(placeholder = "BUY WITH TICKETS", row = 1, options = [
        discord.SelectOption(label = "Chips", value = "chips"),
        discord.SelectOption(label = "Dice", value = "dice"),
        discord.SelectOption(label = "Tiles", value = "tiles")
    ])

    tokensSelect = discord.ui.Select(placeholder = "BUY WITH TOKENS", row = 2, options = [
        discord.SelectOption(label = "Dominoes", value = "dominoes"),
        discord.SelectOption(label = "Dice", value = "dice"),
        discord.SelectOption(label = "Tiles", value = "tiles"),
        discord.SelectOption(label = "Chits", value = "chits")
    ])

    diceSelect = discord.ui.Select(placeholder = "BUY WITH DICE", row = 1, options = [
        # discord.SelectOption(label = "1wk Queue Priority", value = "priority"),
        discord.SelectOption(label = "5 Hangman Plays", value = "hangman"),
        discord.SelectOption(label = "5 2048 Plays", value = "2048"),
        discord.SelectOption(label = "Small Pack", value = "small"),
        discord.SelectOption(label = "Large Pack", value = "large"),
        discord.SelectOption(label = "Premium Pack", value = "premium")
    ])

    dominoSelect = discord.ui.Select(placeholder = "BUY WITH DOMINOES", row = 1, options = [
        discord.SelectOption(label = "None Available", value = "none"),
        # discord.SelectOption(label = "", value = ""),
        # discord.SelectOption(label = "", value = ""),
        # discord.SelectOption(label = "", value = ""),
        # discord.SelectOption(label = "", value = ""),
        # discord.SelectOption(label = "", value = "")
    ])

    tileSelect = discord.ui.Select(placeholder = "BUY WITH TILES", row = 1, options = [
        discord.SelectOption(label = "None Available", value = "none"),
        # discord.SelectOption(label = "", value = ""),
        # discord.SelectOption(label = "", value = ""),
        # discord.SelectOption(label = "", value = ""),
        # discord.SelectOption(label = "", value = ""),
        # discord.SelectOption(label = "", value = "")
    ])

    chitSelect = discord.ui.Select(placeholder = "BUY WITH CHITS", row = 1, options = [
        discord.SelectOption(label = "2x Medals", value = "doubler"),
        # discord.SelectOption(label = "", value = ""),
        # discord.SelectOption(label = "", value = ""),
        # discord.SelectOption(label = "", value = ""),
        # discord.SelectOption(label = "", value = ""),
        # discord.SelectOption(label = "", value = "")
    ])

    currencyView = discord.ui.View(ticketsSelect, tokensSelect)
    diceView     = discord.ui.View(diceSelect)
    dominoView   = discord.ui.View(dominoSelect)
    tileView     = discord.ui.View(tileSelect)
    chitView     = discord.ui.View(chitSelect)

    paginator = Paginator(
        [
            Page(embeds = [discord.Embed(title = "Currency Shop", description = "**50 Chips:** 5 🎟️\n**1 Dice:** 456 🎟️ or 142 🪙\n**1 Domino:** 325 🪙\n**1 Tile** 245 🎟️ or 76 🪙\n**Chit:** 648 🪙\n## Tokens (coming soon)\n**🪙 568:** $2.99 ($0.49 first purchase)\n**🪙 1,687:** $4.99 ($2.99 first purchase)\n**🪙 2,562:** $14.99 ($4.99 first purchase)", color = config.Color.COLORLESS).set_footer(text = config.footer)], custom_view = currencyView),
            Page(embeds = [discord.Embed(title = "Dice Shop",     description = "**1wk Queue Priority:** Queue Coming Soon!\n**5 Hangman Plays:** 1 dice\n**5 2048 Plays:** 1 dice\n## Gridlock Packs\n**Small Pack:** 1 dice\n**Large Pack:** 2 dice\n**Premium Pack:** 3 dice", color = config.Color.COLORLESS).set_footer(text = config.footer)], custom_view = diceView),
            Page(embeds = [discord.Embed(title = "Domino Shop",   description = "**White on Black Packs:** Coming soon!\n**Monopoly Variants:** Coming soon!", color = config.Color.COLORLESS).set_footer(text = config.footer)], custom_view = dominoView),
            Page(embeds = [discord.Embed(title = "Tile Shop",     description = "**Profile Backgrounds:** Coming soon!\n**Holo Arts:** Coming soon!", color = config.Color.COLORLESS).set_footer(text = config.footer)], custom_view = tileView),
            Page(embeds = [discord.Embed(title = "Chit Shop",     description = "**x2 Medals:** 3 Chits\n## Turing (play vs. cpu)\n**Chess:** Coming soon!\n**Checkers:** Coming soon!\n**Monopoly:** Coming soon!\n**BAMBOOZLE!:** Coming soon!\n## Strategy Guides:\n**Chess:** Coming soon!\n**Checkers:** Coming soon!\n**Gridlock:** Coming soon!", color = config.Color.COLORLESS).set_footer(text = config.footer)], custom_view = chitView)
        ],
        show_indicator = True,
        use_default_buttons = False,
        custom_buttons = [
            PaginatorButton("first", label="<<-", style=discord.ButtonStyle.secondary),
            PaginatorButton("prev",  label="<-",  style=discord.ButtonStyle.secondary),

            PaginatorButton("page_indicator", style=discord.ButtonStyle.gray, disabled=True),

            PaginatorButton("next", label="->",  style=discord.ButtonStyle.secondary),
            PaginatorButton("last", label="->>", style=discord.ButtonStyle.secondary),
        ],
    )

    async def ticketsCallback(interaction):
        await interaction.response.defer(ephemeral = True)

        if ticketsSelect.values[0] == "chips" and user.tickets >= 5:
            user.tickets -= 5
            user.chips += 50
            user.save()
        
        if ticketsSelect.values[0] == "dice" and user.tickets >= 456:
            user.tickets -= 456
            user.dice += 1
            user.save()
        
        if ticketsSelect.values[0] == "tiles" and user.tickets >= 245:
            user.tickets -= 245
            user.tiles += 1
            user.save()
    
    async def tokensCallback(interaction):
        await interaction.response.defer(ephemeral = True)

        if ticketsSelect.values[0] == "dice" and user.tickets >= 142:
            user.tickets -= 142
            user.dice += 1
            user.save()

        if ticketsSelect.values[0] == "dominoes" and user.tickets >= 325:
            user.tickets -= 325
            user.dominoes += 50
            user.save()
        
        if ticketsSelect.values[0] == "tiles" and user.tickets >= 76:
            user.tickets -= 76
            user.tiles += 1
            user.save()

        if ticketsSelect.values[0] == "chits" and user.tickets >= 648:
            user.tickets -= 648
            user.chits += 1
            user.save()

    async def diceCallback(interaction):
        await interaction.response.defer(ephemeral = True)

        if ticketsSelect.values[0] == "priority" and user.dice >= 142:
            # user.dice -= 1
            user.dice += 1
            user.save()

        if ticketsSelect.values[0] == "hangman" and user.dice >= 325:
            user.dice -= 1
            user.plays["hangman"] += 5
            user.save()
        
        if ticketsSelect.values[0] == "2048" and user.dice >= 76:
            user.dice -= 1
            user.plays["2048"] += 5
            user.save()

        if ticketsSelect.values[0] == "small" and user.dice >= 648:
            user.dice -= 1
            user.packs[gridlock.Pack.SMALL] += 1
            user.save()

        if ticketsSelect.values[0] == "large" and user.dice >= 648:
            user.dice -= 2
            user.packs[gridlock.Pack.LARGE] += 1
            user.save()
        
        if ticketsSelect.values[0] == "premium" and user.dice >= 648:
            user.dice -= 3
            user.packs[gridlock.Pack.PREMIUM] += 1
            user.save()
    
    async def dominoesCallback(interaction):
        await interaction.response.defer(ephemeral = True)
    
    async def tilesCallback(interaction):
        await interaction.response.defer(ephemeral = True)

    async def chitsCallback(interaction):
        await interaction.response.defer(ephemeral = True)

        if ticketsSelect.values[0] == "dice" and user.chits >= 5 and user.endorses == 1:
            user.chits -= 5
            user.endorses = 2
            user.save()

    ticketsSelect.callback, tokensSelect.callback, diceSelect.callback, dominoSelect.callback, tileSelect.callback, chitSelect.callback = ticketsCallback, tokensCallback, diceCallback, dominoesCallback, tilesCallback, chitsCallback    
    await paginator.respond(ctx.interaction, ephemeral = True)
    
# TODO: guides command
    
@bot.slash_command(name = "settings", description = "View and modify server settings.")
async def settingsCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    guild = Guild(ctx.guild.id)
    message = None
    select = discord.ui.Select(placeholder = "Modify a setting", options = [discord.SelectOption(label = "Content Sharing", value = "sharing")])

    async def selectCallback(interaction):
        await interaction.response.defer(ephemeral = not show)

        match select.values[0]:
            case "sharing": 
                if interaction.user.id != ctx.guild.owner.id:
                    await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.PERMISSION.value, color = config.Color.ERROR).set_footer(text = f"Version: {config.version}"), ephemeral = True)
                    return
                
                guild.sharing = not guild.sharing
                guild.save()

                await message.edit(embed = discord.Embed(title = f"{ctx.guild.name} Settings", description = "**Content Sharing**: " + ("Enabled" if guild.sharing else "Disabled"), color = config.Color.COLORLESS).set_footer(text = f"Version: {config.version}"))

    select.callback = selectCallback
    message = await ctx.interaction.followup.send(embed = discord.Embed(title = f"{ctx.guild.name} Settings", description = "**Content Sharing**: " + ("Enabled" if guild.sharing else "Disabled"), color = config.Color.COLORLESS).set_footer(text = f"Version: {config.version}"), view = discord.ui.View(select))

@bot.slash_command(name = "leaderboard", description = "See how you stack up against other server members!")
async def leaderboardCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)
    board = ""
    n = 1

    for i in Guild(ctx.guild.id).users[0:20]: 
        user = User(i)
        name = await bot.fetch_user(i)
        name = name.name
        xp = ""
        # TODO: actually order the leaderboard
        for i in range(10): xp += "▰" if i < round((user.xp / user.get_next_level()) * 10) else "▱"
        board += f"\n[{n}] ‣ **{name} (Level {user.get_level()}):** {user.xp} xp `{xp}`"
        n += 1
    
    await ctx.interaction.followup.send(embed = discord.Embed(title = f"{ctx.guild.name} Leaderboard", description = board, color = config.Color.COLORLESS).set_footer(text = f"Version: {config.version}"))

@bot.slash_command(name = "credits", description = "A lot of cool people are behind this project!")
async def creditsCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)
    str = ""

    for i in config.credits.keys(): str += f"{i}: {config.credits[i]}\n"
    embed = discord.Embed(title = "Contributors:", description = str, color = config.Color.COLORLESS).set_footer(text = f"Version: {config.version}")
    await ctx.interaction.followup.send(embed = embed)
    
@bot.slash_command(name = "support", description = "Need a hand?")
async def supportCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)
    embed = discord.Embed(title = "Support", description = "Use `/help` to learn how to use my commands or `/info` to learn about my games. If you need further support, have suggestions, or want to report a bug, join our support server:", color = config.Color.COLORLESS).set_footer(text = config.footer).set_thumbnail(url = "https://cdn.discordapp.com/icons/1101982625003995270/a_ee9d87e8365151c5940a2de8aea51c06.webp")
    await ctx.interaction.followup.send(view = discord.ui.View(discord.ui.Button(label = "Join", url = "https://discord.gg/CfPYvDZ6rF", style = discord.ButtonStyle.success)), embed = embed)

# TODO: user commands
@bot.user_command(name="View Profile")
async def profileUserCommand(ctx, user: discord.Member):
    await ctx.defer(ephemeral = True)
    if user is None: user = ctx.author
    u: User = User(user.id, Guild(ctx.guild.id))

    moreSelect = discord.ui.Select(placeholder = "See More...", options = [
        discord.SelectOption(label = "Titles", value = "titles"),
        discord.SelectOption(label = "Backgrounds", value = "backgrounds"),
        discord.SelectOption(label = "Holo Cards", value = "holos"),
        discord.SelectOption(label = "CAH Packs", value = "whiteonblack"),
        discord.SelectOption(label = "monopoly Variants", value = "monopoly"),
        discord.SelectOption(label = "Achievements", value = "achievements"),
        discord.SelectOption(label = "Medals", value = "medals")
    ])

    changeSelect = discord.ui.Select(placeholder = "Change Your...")
    if len(u.titles) > 1: changeSelect.add_option(label = "Title", value = "title")
    if len(u.backgrounds) > 1: changeSelect.add_option(label = "Profile Background", value = "background")

    async def moreCallback(interaction):
        await interaction.response.defer(ephemeral = True)

        match moreSelect.values[0]:
            case "titles": pass
            case "backgrounds": pass
            case "holos": pass
            case "whiteonblack": pass
            case "monopoly": pass
            case _: pass

    async def changeCallback(interaction):
        await interaction.response.defer(ephemeral = True)
        
        match changeSelect.values[0]:
            case "title": pass
            case "background": pass
            case _: pass

    moreSelect.callback   = moreCallback
    changeSelect.callback = changeCallback

    view = discord.ui.View(moreSelect)
    if user == ctx.author and len(changeSelect.options) > 0: view.add_item(changeSelect)

    xp_str = ""
    titles_str = ""
    guides_str = ""
    variant_str = ""
    expansion_str = ""
    gridlock_holos = 0
    bamboozle_holos = 0

    for i in range(10): xp_str += "▰" if i < round((u.xp / u.get_next_level()) * 10) else "▱"
    for i in u.variants: variant_str += f", {i.value}"
    for i in u.expansions: expansion_str += f"{i.value}, "
    for i in u.card_holos: gridlock_holos += 1 if type(i) == gridlock.Game.Card else 0
    for i in u.card_holos: bamboozle_holos += 1 if type(i) == bamboozle.Game.Role else 0

    for i in u.titles:  
        if u.titles.index(i) <= 4: titles_str += f", \"{i}\""
        else:
            titles_str += f", and **{len(u.titles) - u.titles.index(i)}** more"
            break
    
    for i in u.guides:  
        if u.guides.index(i) <= 4: guides_str += f", {i}"
        else:
            guides_str += f", and **{len(u.guides) - u.guides.index(i)}** more"
            break

    if len(variant_str) > 0: variant_str = variant_str[:-2]
    else: variant_str = "None"

    if len(expansion_str) > 0: expansion_str = expansion_str[:-2]
    else: expansion_str = "None"

    embed = discord.Embed(title = user.name + (" ⭐" if u.subscribed_since else " ") + f" (player since <t:{u.join}:D>)", description = f"**Tickets:** {u.tickets}\n**Tokens:** {u.tokens}\n**Chips:** {u.chips}\n\n**Dice:** {u.dice}\n**Dominoes:** {u.dominoes}\n**Tiles:** {u.tiles}\n**Chits:** {u.chits}\n\n**Endorsements:** {u.endorsements}\n**Level:** {u.get_level()} | **XP:** {u.xp} `{xp_str}`\n**Turing Progress:** {len(u.turing)} / 6\n\n**Achievements:** {u.achievement_str('theadas')}", color = config.Color.COLORLESS).set_footer(text = config.footer)

    if u.stats["2048"]["games"] > 0: embed.add_field(name = '2048',  value = f"Games Played: {u.stats['2048']['games']}\n\nAchievements: {u.achievement_str('2048')}", inline = False)
    if u.stats["bamboozle"]["wins"] + u.stats["bamboozle"]["losses"] > 0: embed.add_field(name = "BAMBOOZLE!", value = f"Skill Rating (SR): {math.floor(u.sr['bamboozle'])}\nGames Played: {u.stats['bamboozle']['wins'] + u.stats['bamboozle']['losses']}\nGames Won: {u.stats['bamboozle']['wins']} ({math.floor(u.stats['bamboozle']['wins'] / (u.stats['bamboozle']['wins'] + u.stats['bamboozle']['losses'])) * 100})% Winrate\nHolo Cards Owned: {bamboozle_holos}\n\nAchievements: {u.achievement_str('bamboozle')}\nMedals: ```Manipulator: {u.stats['bamboozle']['medals']['manipulator']}\nPoker Face: {u.stats['bamboozle']['medals']['poker face']}\nBackstabber: {u.stats['bamboozle']['medals']['backstabber']}```", inline = False)
    if u.stats["blackjack"]["wins"] + u.stats["blackjack"]["losses"] > 0: embed.add_field(name = "Blackjack",  value = f"Games Played: {u.stats['blackjack']['wins'] + u.stats['blackjack']['losses']}\n\nAchievements: {u.achievement_str('blackjack')}", inline = False)
    if u.stats["whiteonblack"]["games"] > 0: embed.add_field(name = "White on Black",  value = f"Games Played: {u.stats['whiteonblack']['games']}\n\nExpansions Owned: {expansion_str}\nAchievements: {u.achievement_str('whiteonblack')}\nMedals: ```Lucky: {u.stats['whiteonblack']['medals']['lucky']}\nFunny: {u.stats['whiteonblack']['medals']['funny']}\nNasty: {u.stats['whiteonblack']['medals']['nasty']}\nOffensive: {u.stats['whiteonblack']['medals']['offensive']}```", inline = False)
    if u.stats["checkers"]["wins"] + u.stats["checkers"]["losses"] > 0: embed.add_field(name = "Checkers",  value = f"Skill Rating (SR): {math.floor(u.sr['checkers'])}\nGames Played: {u.stats['checkers']['wins'] + u.stats['checkers']['losses']}\nGames Won: {u.stats['checkers']['wins']} ({math.floor(u.stats['checkers']['wins'] / (u.stats['checkers']['wins'] + u.stats['checkers']['losses'])) * 100})% Winrate\n\nAchievements: {u.achievement_str('checkers')}\nMedals: ```Played Well: {u.stats['checkers']['medals']['played well']}```", inline = False)
    if u.stats["chess"]["wins"] + u.stats["chess"]["losses"] > 0: embed.add_field(name = "Chess",  value = f"Skill Rating (SR): {math.floor(u.sr['chess'])}\nGames Played: {u.stats['chess']['wins'] + u.stats['chess']['losses']}\nGames Won: {u.stats['chess']['wins']} ({math.floor(u.stats['chess']['wins'] / (u.stats['chess']['wins'] + u.stats['chess']['losses'])) * 100})% Winrate\n\nAchievements: {u.achievement_str('chess')}\nMedals: ```Knowledgeable: {u.stats['chess']['medals']['knowledgeable']}\nRisk Taker: {u.stats['chess']['medals']['risk taker']}\nPlayed fast: {u.stats['chess']['medals']['played Fast']}```", inline = False)
    if u.stats["gridlock"]["wins"] + u.stats["gridlock"]["losses"] > 0: embed.add_field(name = "Gridlock",  value = f"Skill Rating (SR): {math.floor(u.sr['gridlock'])}\nGames Played: {u.stats['gridlock']['wins'] + u.stats['gridlock']['losses']}\nGames Won: {u.stats['gridlock']['wins']} ({math.floor(u.stats['gridlock']['wins'] / (u.stats['gridlock']['wins'] + u.stats['gridlock']['losses'])) * 100})% Winrate\nHolo Cards Owned: {gridlock_holos}\n**Packs:** {u.packs[gridlock.Pack.SMALL]} Small, {u.packs[gridlock.Pack.LARGE]} Large, {u.packs[gridlock.Pack.PREMIUM]} Premium\n\nAchievements: {u.achievement_str('gridlock')}\nMedals: ```Interesting Deck: {u.stats['gridlock']['medals']['interesting deck']}\nPlayed Well: {u.stats['gridlock']['medals']['played well']}\nPlayed Fast: {u.stats['gridlock']['medals']['played fast']}```", inline = False)
    if u.stats["hangman"]["wins"] + u.stats["hangman"]["losses"] > 0: embed.add_field(name = "Hangman",  value = f"Games Played: {u.stats['hangman']['wins'] + u.stats['hangman']['losses']}\n\nGames Won: {u.stats['hangman']['wins']} ({math.floor(u.stats['hangman']['wins'] / (u.stats['hangman']['wins'] + u.stats['hangman']['losses'])) * 100})% Winrate\n\nAchievements: {u.achievement_str('hangman')}", inline = False)
    if u.stats["monopoly"]["wins"] + u.stats["monopoly"]["losses"] > 0: embed.add_field(name = "monopoly",  value = f"Games Played: {u.stats['monopoly']['wins'] + u.stats['monopoly']['losses']}\nGames Won: {u.stats['monopoly']['wins']} ({math.floor(u.stats['monopoly']['wins'] / (u.stats['monopoly']['wins'] + u.stats['monopoly']['losses'])) * 100})% Winrate\n\nVariants Owned: {variant_str}\nAchievements: {u.achievement_str('monopoly')}\nMedals: ```Lucky: {u.stats['monopoly']['medals']['lucky']}\nSmart Investor: {u.stats['monopoly']['medals']['smart investor']}\nNegotiator: {u.stats['monopoly']['medals']['negotiator']}```", inline = False)
    if u.stats["rps"]["wins"] + u.stats["rps"]["losses"] > 0: embed.add_field(name = "Rock Paper Scissors",  value = f"Games Played: {u.stats['rps']['wins'] + u.stats['rps']['losses']}\n\nGames Won: {u.stats['rps']['wins']} ({math.floor(u.stats['rps']['wins'] / (u.stats['rps']['wins'] + u.stats['rps']['losses'])) * 100})% Winrate\n\nAchievements: {u.achievement_str('rps')}", inline = False)
    if u.stats["slots"]["wins"] + u.stats["slots"]["losses"] > 0: embed.add_field(name = "Blackjack",  value = f"Games Played: {u.stats['slots']['wins'] + u.stats['slots']['losses']}\n\nAchievements: {u.achievement_str('slots')}", inline = False)
    if u.stats["tictactoe"]["wins"] + u.stats["tictactoe"]["losses"] > 0: embed.add_field(name = "Tic Tac Toe",  value = f"Games Played: {u.stats['tictactoe']['wins'] + u.stats['tictactoe']['losses']}\n\nGames Won: {u.stats['tictactoe']['wins']} ({math.floor(u.stats['tictactoe']['wins'] / (u.stats['tictactoe']['wins'] + u.stats['tictactoe']['losses'])) * 100})% Winrate\n\nAchievements: {u.achievement_str('tictactoe')}", inline = False)

    await ctx.interaction.followup.send(embed = embed, view = view)

# @bot.user_command(name="Challenge to a Game")
# async def profileUserCommand(ctx, user: discord.Member):
#     await ctx.defer(ephemeral = True)

# ========================================================================================================================
# /help commands
# ========================================================================================================================
    
@help.command(name = "ping")
async def pingHelpCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    embed = discord.Embed(title = "Ping Command", description = "Test the bot's response time.\n**Usage:** /ping", color = config.Color.COLORLESS).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@help.command(name = "profile")
async def profileHelpCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    embed = discord.Embed(title = "Profile Command", description = "View a user's profile. If you do not specify a user, your own will be shown.\n**Usage:** /profile [user]", color = config.Color.COLORLESS).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)
        
@help.command(name = "leaderboard")
async def leaderboardHelpCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    embed = discord.Embed(title = "Leaderboard Command", description = "See how you stack up against other server members!\n**Usage:** /leaderboard", color = config.Color.COLORLESS).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)
        
@help.command(name = "credits")
async def creditsHelpCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    embed = discord.Embed(title = "Credits Command", description = "\n**Usage:** /credits", color = config.Color.COLORLESS).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)
        
@help.command(name = "shop")
async def shopHelpCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    embed = discord.Embed(title = "Shop Command", description = "\n**Usage:** /shop [category]", color = config.Color.COLORLESS).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)
        
@help.command(name = "support")
async def supportHelpCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    embed = discord.Embed(title = "Support Command", description = "\n**Usage:** /support", color = config.Color.COLORLESS).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)
        
@help.command(name = "play")
async def playHelpCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    embed = discord.Embed(title = "Play Command", description = "\n**Usage:** /play <game>", color = config.Color.COLORLESS).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

# ========================================================================================================================
# /info subcommands
# ========================================================================================================================
# @info.command(name = "gamelist")
# async def gamelistCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
#     await ctx.defer(ephemeral = not show)
#     str = ""
#     for i in info.: str += f"\n- {i.name}"

#     embed = discord.Embed(title = "All Games: (use /info <game> for details)", description = str, color = config.Color.COLORLESS)
#   .set_footer(text = config.footer)

#     await ctx.interaction.followup.send(embed = embed)

@info.command(name = "bamboozle")
async def bamboozleInfoCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    embed = discord.Embed(title = "BAMBOOZLE!", description = bamboozle.description, color = config.Color.COLORLESS).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@info.command(name = "blackjack")
async def blackjackInfoCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    embed = discord.Embed(title = "Blackjack", description = blackjack.description, color = config.Color.COLORLESS).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@info.command(name = "whiteonblack")
async def whiteonblackInfoCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    embed = discord.Embed(title = "White on Black", description = whiteonblack.description, color = config.Color.COLORLESS).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@info.command(name = "checkers")
async def checkersInfoCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    embed = discord.Embed(title = "Checkers", description = checkers.description, color = config.Color.COLORLESS).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@info.command(name = "chess")
async def chessInfoCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    embed = discord.Embed(title = "Chess", description = chess.description, color = config.Color.COLORLESS).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@info.command(name = "gridlock")
async def gridlockInfoCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    embed = discord.Embed(title = "Gridlock", description = gridlock.description, color = config.Color.COLORLESS).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@info.command(name = "hangman")
async def hangmanInfoCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    embed = discord.Embed(title = "Hangman", description = hangman.description, color = config.Color.COLORLESS).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@info.command(name = "holdem")
async def holdemInfoCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    embed = discord.Embed(title = "Holdem", description = holdem.description, color = config.Color.COLORLESS).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@info.command(name = "monopoly")
async def monopolyInfoCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    embed = discord.Embed(title = "monopoly", description = monopoly.description, color = config.Color.COLORLESS).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@info.command(name = "rockpaperscissors")
async def rockpaperscissorsInfoCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    embed = discord.Embed(title = "Rock Paper Scissors", description = rps.description, color = config.Color.COLORLESS).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@info.command(name = "slots")
async def slotsInfoCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    embed = discord.Embed(title = "Slots", description = slots.description, color = config.Color.COLORLESS).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@info.command(name = "tictactoe")
async def tictactoeInfoCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    embed = discord.Embed(title = "Tic Tac Toe", description = tictactoe.description, color = config.Color.COLORLESS).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@info.command(name = "twentyfortyeight")
async def twentyfortyeightInfoCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)

    embed = discord.Embed(title = '2048', description = twentyfortyeight.description, color = config.Color.COLORLESS).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

# ========================================================================================================================
# /game commands
# ========================================================================================================================
@play.command(name = "bamboozle", description = "Fight to accomplish the goals of your secret role without getting lynched!")
async def bamboozleGameCommand(ctx):
    await ctx.defer(ephemeral = False)

    embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@play.command(name = "blackjack", description = "Draw cards from the deck, trying to be closest to 21 without going over.")
async def blackjackGameCommand(ctx, bet: discord.Option(int, "Bet an amount between 2 and 500 chips.")):
    await ctx.defer(ephemeral = True)
    user = User(ctx.author.id)

    if user.chips < bet: await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_ENOUGH.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
    else:
        g = blackjack.Game(user, bet)
        e, v = g.render()

        g.message = await ctx.interaction.followup.send(embed = e, view = v)
    
@play.command(name = "whiteonblack", description = "Find the funniest response to the Czar\'s prompts!")
# @discord.is_nsfw()
async def whiteonblackGameCommand(ctx):
    await ctx.defer()

    embed = discord.Embed()
    user = User(ctx.author.id, Guild(ctx.guild_id))

    if user.game() is not None: 
        g = user.game()
        c, e, v = g.render()
        g.message = await ctx.interaction.followup.send(content = c, embeds = e, view = v)
        user.save()
    
    else:
        view = discord.ui.View(timeout = None)
        players = [ctx.author]
        message = None

        embed.title = "Play White on Black!"
        embed.description = f"{ctx.author.mention} is starting a game. Click `JOIN` to join the game or `LEAVE` to leave it. Use `/info whiteonblack` to learn the basics of the game. When there are 2-10 players in the game, {ctx.author.mention} can use `START` to start the game. They can also cancel the game by deleting this message.\n\nCurrent players:\n- {ctx.author.mention}"

        embed.color  = config.Color.COLORLESS
        embed.set_footer(text = config.footer)

        joinButton   = discord.ui.Button(style = discord.ButtonStyle.secondary, label = "JOIN")
        leaveButton  = discord.ui.Button(style = discord.ButtonStyle.secondary, label = "LEAVE")
        cancelButton = discord.ui.Button(style = discord.ButtonStyle.danger,    label = "CANCEL")
        startButton  = discord.ui.Button(style = discord.ButtonStyle.success,   label = "START", disabled = True)

        async def joinCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user in players or User(interaction.user.id, Guild(ctx.guild_id)).game(): await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.IN_GAME.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)

            if len(players) >= 10:
                e = discord.Embed()

                e.title       = random.choice(config.error_titles)
                e.description = config.Error.GENERIC.value
                e.color       = config.Color.ERROR
                e.set_footer(text = config.footer)

                await interaction.followup.send(embed = e, ephemeral = True)
                return

            players.append(interaction.user)
            embed.description += f"\n- {interaction.user.mention}"
            startButton.disabled = True if 3 <= len(players) >= 10 else False

            await interaction.edit_original_response(embed = embed, view = view)

        async def leaveCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user.id == players[0]:
                e = discord.Embed()

                e.title       = random.choice(config.error_titles)
                e.description = config.Error.GENERIC.value
                e.color       = config.Color.ERROR
                e.set_footer(text = config.footer)

                await interaction.followup.send(embed = e, ephemeral = True)
                return
            
            if interaction.user.id in players:
                players.remove(interaction.user.id)
                embed.description -= f"\n- {interaction.user.mention}"
                startButton.disabled = True if 2 <= len(players) >= 10 else False

                await interaction.edit_original_response(embed = embed, view = view)

            else:
                e = discord.Embed()

                e.title       = random.choice(config.error_titles)
                e.description = config.Error.GENERIC.value
                e.color       = config.Color.ERROR
                e.set_footer(text = config.footer)

                await interaction.followup.send(embed = e, ephemeral = True)
                return

        async def cancelCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user is not ctx.author:
                embed.title       = random.choice(config.error_titles)
                embed.description = config.Error.PERMISSION.value
                embed.color       = config.Color.ERROR
                embed.set_footer(text = config.footer)

                await ctx.interaction.followup.send(embed = embed, ephemeral = True)

            else: await message.delete()

        async def startCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user == players[0]:
                g = whiteonblack.Game([whiteonblack.Player(i.id, i.name) for i in players])
                c, e, v = g.render()

                await message.delete()
                g.message = await ctx.interaction.followup.send(content = c, embeds = e, view = v)

            else:
                e = discord.Embed()

                e.title       = random.choice(config.error_titles)
                e.description = config.Error.PERMISSION.value
                e.color       = config.Color.ERROR
                e.set_footer(text = config.footer)

                await interaction.followup.send(embed = e, ephemeral = True)

        joinButton.callback   = joinCallback
        leaveButton.callback  = leaveCallback
        cancelButton.callback = cancelCallback
        startButton.callback  = startCallback

        view.add_item(joinButton)
        view.add_item(leaveButton)
        view.add_item(cancelButton)
        view.add_item(startButton)

        message = await ctx.interaction.followup.send(embed = embed, view = view)

@play.command(name = "checkers", description = "Capture all your opponent's pieces to claim victory!")
async def checkersGameCommand(ctx):
    await ctx.defer(ephemeral = False)

    embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@play.command(name = "chess", description = "Battle it out in this classic game of strategy")
async def chessGameCommand(ctx):
    await ctx.defer(ephemeral = False)

    embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@play.command(name = "gridlock", description = "Collect cards and play them on a 5x5 grid to outsmart your opponents!")
async def gridlockGameCommand(ctx):
    await ctx.defer(ephemeral = False)

    embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@play.command(name = "hangman", description = "Try and guess a word before you get hanged!")
async def hangmanGameCommand(ctx):
    await ctx.defer(ephemeral = True)
    user = User(ctx.author.id)

    if user.plays["hangman"] < 1: await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_ENOUGH.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
    else:
        g = hangman.Game(user)
        e, v = g.render()
        g.message = await ctx.interaction.followup.send(embed = e, view = v)

@play.command(name = "holdem", description = "Get lucky and bluff your friends to win big!")
async def holdemGameCommand(ctx):
    await ctx.defer(ephemeral = False)

    embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@play.command(name = "monopoly", description = "Race other players to buy up properties without going bankrupt!")
async def monopolyGameCommand(ctx):
    await ctx.defer(ephemeral = False)
    user = User(ctx.author.id, Guild(ctx.guild.id))

    if user.game() != None:
        g = user.game()
        e, v, f = g.render()
        g.message = await ctx.interaction.followup.send(embed = e, view = v, file = f)
    
    else:
        joinButton   = discord.ui.Button(style = discord.ButtonStyle.secondary, label = "JOIN")
        leaveButton  = discord.ui.Button(style = discord.ButtonStyle.secondary, label = "LEAVE")
        cancelButton = discord.ui.Button(style = discord.ButtonStyle.danger,    label = "CANCEL")
        startButton  = discord.ui.Button(style = discord.ButtonStyle.success,   label = "START", disabled = True)

        players = [ctx.author]
        message = None
        embed = discord.Embed(title = "Play Monopoly!", description = f"{ctx.author.mention} is starting a game. Press `JOIN` to join the game or `LEAVE` to leave it. Use `/info monopoly` to learn the basics of the game. When there are 2-8 players in the game, {ctx.author.mention} can use `START` to start the game. They can also `CANCEL` the game at any time.\n\nCurrent players:\n- {ctx.author.mention}", color  = config.Color.HELLARED).set_footer(text = config.footer)
        view = discord.ui.View(joinButton, leaveButton, cancelButton, startButton, timeout = None)

        async def joinCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user in players or User(interaction.user.id).game() != None:
                await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.IN_GAME.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                return

            if len(players) >= 8:
                await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.GENERIC.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                return

            players.append(interaction.user)
            embed.description += f"\n- {interaction.user.mention}"
            startButton.disabled = True if 2 <= len(players) >= 8 else False

            await interaction.edit_original_response(embed = embed, view = view)

        async def leaveCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user.id == players[0]:
                await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.GENERIC.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                return
            
            if interaction.user.id in players and User(interaction.user.id).game():
                players.remove(interaction.user.id)
                embed.description -= f"\n- {interaction.user.mention}"
                startButton.disabled = True if 2 <= len(players) >= 8 else False

                await interaction.edit_original_response(embed = embed, view = view)

            else:
                await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IN_GAME.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                return

        async def cancelCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user is not ctx.author:
                await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IN_GAME.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                return

            else: await message.delete()

        async def startCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user == players[0]:
                g = monopoly.Game([monopoly.Player(i.id, i.name) for i in players])

                await message.delete()
                e, v, f = g.render()
                g.message = await ctx.interaction.followup.send(embed = e, view = v, file = f)

            else:
                await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.PERMISSION.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                return

        joinButton.callback   = joinCallback
        leaveButton.callback  = leaveCallback
        cancelButton.callback = cancelCallback
        startButton.callback  = startCallback

        message = await ctx.interaction.followup.send(embed = embed, view = view)

@play.command(name = "rockpaperscissors", description = "Rock beats scissors, paper beats rock, and scissors beat paper.")
async def rockpaperscissorsGameCommand(ctx):
    await ctx.defer(ephemeral = False)

    embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@play.command(name = "slots", description = "Get 3 in a row to win big!")
async def slotsGameCommand(ctx):
    await ctx.defer(ephemeral = False)

    embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@play.command(name = "tictactoe", description = "Get 3 in a row before your opponent can.")
async def tictactoeGameCommand(ctx):
    await ctx.defer(ephemeral = False)

    embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer)

    await ctx.interaction.followup.send(embed = embed)

@play.command(name = "twentyfortyeight", description = "Merge tiles until you run out of space.")
async def twentyfortyeightGameCommand(ctx):
    await ctx.defer(ephemeral = True)
    user = User(ctx.author.id)

    if user.plays["2048"] < 1: await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_ENOUGH.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
    else:
        g = twentyfortyeight.Game(user)
        e, v, f = g.render()
        g.message = await ctx.interaction.followup.send(embed = e, view = v, file = f)

if __name__ == "__main__":
    bot.run(config.token)