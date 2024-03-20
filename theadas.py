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
from discord.ext import tasks
from discord.ext.pages import Page, Paginator, PaginatorButton

import math, random, os, pickle, asyncio
from enum     import Enum
from datetime import datetime
from typing   import List

_games = []
if __name__ == "__main__":
    import games.bamboozle        as bamboozle
    import games.blackjack        as blackjack
    import games.whiteonblack     as whiteonblack
    import games.checkers         as checkers
    import games.chess            as chess
    import games.gridlock         as gridlock
    import games.hangman          as hangman
    import games.holdem           as holdem
    import games.trust            as trust
    import games.rps              as rps
    import games.slots            as slots
    import games.tictactoe        as tictactoe
    import games.twentyfortyeight as twentyfortyeight

    _games = [
        bamboozle,
        blackjack,
        whiteonblack,
        checkers,
        chess,
        gridlock,
        hangman,
        holdem,
        trust,
        rps,
        slots,
        tictactoe,
        twentyfortyeight
    ]

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
    def __init__(self, id):
        self.id = id
        if not os.path.exists(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p"): pickle.dump(None, open(f"{os.path.join(os.path.dirname(__file__), 'data/games')}/{self.id}.p", "wb"))
        
        try: self.join: float = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).join
        except: self.join: float = math.floor(datetime.now().timestamp())

        try: self.subscribed_since: float = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).subscribed_since
        except: self.subscribed_since: float = None

        try: self.joined: bool = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).joined
        except: self.joined: bool = False

        try: self.priority_until: float = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).priority_until
        except: self.priority_until: float = None

        try: self.endorses: int = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).endorses
        except: self.endorses: int = 1
        
        try: self.medals_given: List[str] = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).medals_given
        except: self.medals_given: List[str] = 0
        
        try: self.endorses_given: List[str] = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).endorses_given
        except: self.endorses_given: List[str] = 0
        
        try: self.claimed: bool = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).claimed
        except: self.claimed: bool = False

        try: self.titles: List[str] = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).titles
        except: self.titles: List[str] = ["Novice"]
        
        try: self.backgrounds: List[str] = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).backgrounds
        except: self.backgrounds: List[str] = ["assets/default_background.png"]
        
        try: self.turing: List[str] = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).turing
        except: self.turing: List[str] = ["whiteonblack"]
        
        try: self.guides: List[str] = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).guides
        except: self.guides: List[str] = ["2048", "checkers"]
        
        try: self.card_holos: List[gridlock.Game.Card | bamboozle.Game.Role] = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).card_holos
        except: self.card_holos: List[gridlock.Game.Card | bamboozle.Game.Role]  = []
        
        try: self.expansions: List[whiteonblack.Expansion] = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).expansions
        except: self.expansions: List[whiteonblack.Expansion] = [whiteonblack.Expansion.BASE]
        
        try: self.variants: List[trust.Variant] = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).variants
        except: self.variants: List[trust.Expansion] = [trust.Variant.BASE]
        
        try: self.tickets: int = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).tickets
        except: self.tickets: int = 200
        
        try: self.tokens: int = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).tokens
        except: self.tokens: int = 0
        
        try: self.chips: int = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).chips
        except: self.chips: int = 500
        
        try: self.xp: int = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")). xp
        except: self.xp: int = 0
        
        try: self.endorsements: int = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).endorsements
        except: self.endorsements: int = 0
        
        try: self.dice: int = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).dice
        except: self.dice: int = 0 # consumables, 456 🎟️ or 142 🪙
        
        try: self.dominoes: int = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).dominoes
        except: self.dominoes: int = 0 # variants, 325 🪙
        
        try: self.tiles: int = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).tiles
        except: self.tiles: int = 0 # cosmetics, 245 🎟️ or 76 🪙
        
        try: self.chits: int = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).chits
        except: self.chits: int = 0 # qol, 648 🪙
        
        try: self.sr: dict = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).sr
        except: self.sr = {
            "bamboozle": 100,
            "checkers": 100,
            "chess": 100,
            "gridlock": 100
        }
            
        try: self.plays: dict = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).plays
        except: self.plays = {
            "2048": 3,
            "hangman": 3
        }
            
        try: self.packs: dict = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).packs
        except: self.packs = {
            gridlock.Pack.SMALL: 0,
            gridlock.Pack.LARGE: 1,
            gridlock.Pack.PREMIUM: 0
        }
            
        try: self.achievements: dict = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).achievements
        except: self.achievements = {
            "theadas": [],
            "bamboozle": [],
            "blackjack": [],
            "whiteonblack": [],
            "checkers": [],
            "chess": [],
            "gridlock": [],
            "hangman": [],
            "holdem": [],
            "trust": [],
            "rps": [],
            "slots": [],
            "tictactoe": [],
            "2048": []
        }
            
        try: self.stats: dict = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/users')}/{id}.p", "rb")).stats
        except: self.stats = {
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

            "trust": {
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

        self.save()
    
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
        guild = None

        if os.path.exists(f"{os.path.join(os.path.dirname(__file__), 'data/guilds')}/{id}.p"):
            guild: Guild = pickle.load(open(f"{os.path.join(os.path.dirname(__file__), 'data/guilds')}/{id}.p", "rb"))

        try: self.sharing: bool = guild.sharing
        except: self.sharing: bool = False

        self.save()

    def save(self): pickle.dump(self, open(f"{os.path.join(os.path.dirname(__file__), 'data/guilds')}/{self.id}.p", "wb"))
intents = discord.Intents()
intents.members = True
intents.guilds = True
intents.message_content = True
intents.guild_messages = True
intents.guild_reactions = True
bot = discord.Bot(activity = discord.Game("Play games with friends!"), intents = intents)

@tasks.loop(hours = 24)
async def reset_plays():
    for i in os.listdir("data/users"):
        if i.endswith(".p"):
            user = User(i.split(".")[0])

            user.plays["2048"] += (3 if user.plays["2048"] <= 0 else 0)
            user.plays["hangman"] += (3 if user.plays["hangman"] <= 0 else 0)
            user.chips += (100 if user.chips <= 0 else 0)

@bot.event
async def on_ready():
    await bot.register_commands(delete_existing = True)
    reset_plays.start()

@bot.event
async def on_member_join(member: discord.Member):
    if member.guild.id != 1101982625003995270 or member.bot: return
    else:
        user = User(member.id)
        if user.joined: 
            channel: discord.TextChannel = await bot.fetch_channel(1101989112619204689)
            await channel.send(f"Look! The portal is glowing! It's {member.mention}!")
        else:
            xp, tickets, jackpot = user.award()
            channel: discord.TextChannel = await bot.fetch_channel(1101989112619204689)
            await channel.send(embed = discord.Embed(title = f"Look! The portal is glowing! It's {member.name}!", description = f"For joining the support server, they received **{xp}** experience and **{tickets}** tickets." + (f"\n**JACKPOT!**\nThey also got {jackpot}!" if jackpot else ""), color = 0x229acc).set_footer(text = config.footer))
            
            user.joined = True
            user.save()

@bot.event
async def on_raw_member_remove(data):
    guild = await bot.fetch_guild(data.guild_id)
    if guild.id != 1101982625003995270 or data.user.bot: return
    else: 
        channel: discord.TextChannel = await bot.fetch_channel(1101989112619204689)
        await channel.send(f"{data.user.name} vanished...")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot: return
    else: 
        user = User(message.author.id)
        level = user.get_level()

        user.xp += 1
        user.save()

        if user.get_level() > level: await message.channel.send(embed = discord.Embed(title = f"{message.author.name} is now Level {user.get_level()}!", color = config.Color.COLORLESS).set_footer(text = config.footer))

play = bot.create_group("play", "Play a game!")

@bot.slash_command(name = "ping", description = "Test the bot's latency.")
async def pingCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)
    if ctx.author.bot: return

    embed = discord.Embed(title = "Pong!", description = f"The bot's latency is currently {round(bot.latency, 2)}ms.").set_footer(text = config.footer)

    if bot.latency > 30: embed.color = discord.Color.red()
    else: embed.color = discord.Color.green()

    await ctx.interaction.followup.send(embed = embed)

@bot.slash_command(name = "summon", description = "Spend dice for a chance to win cool items!")
async def summonCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)
    if ctx.author.bot: return

    message: discord.Message = None
    domainSelect = discord.ui.Select(placeholder = "PICK A DOMAIN TO SUMMON FROM", options = [
        discord.SelectOption(label = "Logos", value = "logos"),
        discord.SelectOption(label = "Ethos", value = "ethos"),
        discord.SelectOption(label = "Pathos", value = "pathos")
    ])

    async def domainCallback(interaction):
        await interaction.response.defer(ephemeral = not show)
        user = User(ctx.author.id)

        if interaction.user.id != ctx.author.id:
            await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.PERMISSION.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
            return
        
        match domainSelect.values[0]:
            case "logos":
                user.dice -= 1
                if random.randint(1, 20) == 20:
                    choice = random.choice(["hangman", "2048"])

                    user.plays[choice] += 10
                    user.save()

                    await message.edit(embed = discord.Embed(title = f"{ctx.author.name} is Summoning!", description = f"🐼PANDA!!\nThey summoned **10 {choice} plays**!", color = config.Color.COLORLESS))
                else:
                    tickets  = random.randint(0, 50)
                    tokens   = random.randint(0, 20)
                    chips    = random.randint(0, 100)
                    xp       = random.randint(15, 60)
                    dominoes = random.randint(0, 2)
                    tiles    = random.randint(0, 2)
                    chits    = random.randint(0, 2)

                    user.tickets  += tickets
                    user.tokens   += tokens
                    user.chips    += chips
                    user.xp       += xp
                    user.dominoes += dominoes
                    user.tiles    += tiles
                    user.chits    += chits

                    summon = f"{xp} experience"
                    if tickets >= 0: summon  += f", {tickets} tickets"
                    if tokens >= 0: summon   += f", {tokens} tokens"
                    if chips >= 0: summon    += f", {chips} chips"
                    if dominoes >= 0: summon += f", {dominoes} dominoes"
                    if tiles >= 0: summon    += f", {tiles} tiles"
                    if chits >= 0: summon    += f", {chits} chits"

                    user.save()
                    await message.edit(embed = discord.Embed(title = f"{ctx.author.name} is Summoning!", description = f"They summoned **{summon}**!", color = config.Color.COLORLESS))

            case "ethos":
                user.dice -= 2
                if random.randint(1, 20) == 20:
                    choice = random.choice(["Early Supporter", "Summon Master"])

                    user.titles.append(choice)
                    user.save()

                    await message.edit(embed = discord.Embed(title = f"{ctx.author.name} is Summoning!", description = f"🐼PANDA!!\nThey summoned the **\"{choice}\" title**!", color = config.Color.COLORLESS))
                else:
                    tickets  = random.randint(0, 50)
                    tokens   = random.randint(0, 20)
                    chips    = random.randint(0, 100)
                    xp       = random.randint(15, 60)
                    dominoes = random.randint(0, 2)
                    tiles    = random.randint(0, 2)
                    chits    = random.randint(0, 2)

                    user.tickets  += tickets
                    user.tokens   += tokens
                    user.chips    += chips
                    user.xp       += xp
                    user.dominoes += dominoes
                    user.tiles    += tiles
                    user.chits    += chits

                    summon = f"{xp} experience"
                    if tickets >= 0: summon  += f", {tickets} tickets"
                    if tokens >= 0: summon   += f", {tokens} tokens"
                    if chips >= 0: summon    += f", {chips} chips"
                    if dominoes >= 0: summon += f", {dominoes} dominoes"
                    if tiles >= 0: summon    += f", {tiles} tiles"
                    if chits >= 0: summon    += f", {chits} chits"

                    user.save()
                    await message.edit(embed = discord.Embed(title = f"{ctx.author.name} is Summoning!", description = f"They summoned **{summon}**!", color = config.Color.COLORLESS))
            
            case "pathos":
                user.dice -= 3
                if random.randint(1, 20) == 20:
                    if user.endorses > 1: await message.edit(embed = discord.Embed(title = f"{ctx.author.name} is Summoning!", description = f"🐼PANDA!!\nThey summoned **Double Medals**! (already owned)", color = config.Color.COLORLESS))
                    else:
                        user.endorses = 2
                        user.save()

                        await message.edit(embed = discord.Embed(title = f"{ctx.author.name} is Summoning!", description = f"🐼PANDA!!\nThey summoned the **Double Medals**!", color = config.Color.COLORLESS))
                else:
                    tickets  = random.randint(0, 50)
                    tokens   = random.randint(0, 20)
                    chips    = random.randint(0, 100)
                    xp       = random.randint(15, 60)
                    dominoes = random.randint(0, 2)
                    tiles    = random.randint(0, 2)
                    chits    = random.randint(0, 2)

                    user.tickets  += tickets
                    user.tokens   += tokens
                    user.chips    += chips
                    user.xp       += xp
                    user.dominoes += dominoes
                    user.tiles    += tiles
                    user.chits    += chits

                    summon = f"{xp} experience"
                    if tickets >= 0: summon  += f", {tickets} tickets"
                    if tokens >= 0: summon   += f", {tokens} tokens"
                    if chips >= 0: summon    += f", {chips} chips"
                    if dominoes >= 0: summon += f", {dominoes} dominoes"
                    if tiles >= 0: summon    += f", {tiles} tiles"
                    if chits >= 0: summon    += f", {chits} chits"

                    user.save()
                    await message.edit(embed = discord.Embed(title = f"{ctx.author.name} is Summoning!", description = f"They summoned **{summon}**!", color = config.Color.COLORLESS))     
            case _: pass
        # domain = domainSelect.values[0]

        # smallButton   = discord.ui.Button(label = "SMALL", style = discord.ButtonStyle.secondary)
        # largeButton   = discord.ui.Button(label = "LARGE", style = discord.ButtonStyle.blurple)
        # premiumButton = discord.ui.Button(label = "PREMIUM", style = discord.ButtonStyle.success)

        # async def smallCallback(interaction):
        #     await interaction.response.defer(ephemeral = not show)

        #     await message.edit(embed = discord.Embed(), view = discord.ui.View(smallButton, largeButton, premiumButton))

        # async def largeCallback(interaction):
        #     await interaction.response.defer(ephemeral = not show)

        #     await message.edit(embed = discord.Embed(), view = discord.ui.View(smallButton, largeButton, premiumButton))

        # async def premiumCallback(interaction):
        #     await interaction.response.defer(ephemeral = not show)

        #     await message.edit(embed = discord.Embed(), view = discord.ui.View(smallButton, largeButton, premiumButton))

        # smallButton.callback, largeButton.callback, premiumButton.callback = smallCallback, largeCallback, premiumCallback
        # await message.edit(embed = discord.Embed(), view = discord.ui.View(smallButton, largeButton, premiumButton))

    domainSelect.callback = domainCallback
    message = await ctx.interaction.followup.send(embed = discord.Embed(title = f"{ctx.author.name} is Summoning!", description = "Start your summon by choosing a domain. Domains determine what you can summon if you hit a panda (5% chance). Domains rotate occasionally, so make sure to check back frequently!\n## Domains\n**All domains:** tickets, tokens, xp (guaranteed), chips, dominoes, tiles, chits\n**LOGOS (1 dice):** 10 Hangman plays, 10 2048 plays\n**ETHOS (2 dice)** \"Early Supporter\" title, \"Summon Master\" title\n**PATHOS (3 dice):** award an extra medal each game"), view = discord.ui.View(domainSelect))

@bot.slash_command(name = "hack", description = "Change a user's profile.", guild_ids = [1101982625003995270])
async def hackCommand(ctx, u: discord.Option(discord.User, "User to hack."), field: discord.Option(str, "Which field should be hacked?", choices = ["Tickets", "Tokens", "Chips", "Dice", "Dominoes", "Tiles", "Chits", "Experience", "Turing", "Achievements", "Priority", "Backgrounds", "BAMBOOZLE!", "Checkers", "Chess", "Gridlock", "2048", "Hangman", "Game Purge"])):
    await ctx.defer(ephemeral = True)
    if ctx.author.bot: return

    user: User = User(u.id)
    if user.id in config.owners:
        match field:
            case "Tickets":
                plusOne     = discord.ui.Button(label = "1️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusTen     = discord.ui.Button(label = "🔟", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusFifty   = discord.ui.Button(label = "5️⃣0️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusHundred = discord.ui.Button(label = "1️⃣0️⃣0️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)

                minusOne     = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusTen     = discord.ui.Button(label = "🔟", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusFifty   = discord.ui.Button(label = "5️⃣0️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusHundred = discord.ui.Button(label = "1️⃣0️⃣0️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)

                async def plusOneCallback(_):     
                    user.tickets += 1
                    user.save()
                async def plusTenCallback(_):     
                    user.tickets += 10
                    user.save()
                async def plusFiftyCallback(_):   
                    user.tickets += 50
                    user.save()
                async def plusHundredCallback(_): 
                    user.tickets += 100
                    user.save()

                async def minusOneCallback(_):     user.tickets -= 1
                async def minusTenCallback(_):     user.tickets -= 10
                async def minusFiftyCallback(_):   user.tickets -= 50
                async def minusHundredCallback(_): user.tickets -= 100

                plusOne.callback, plusTen.callback, plusFifty.callback, plusHundred.callback, minusOne.callback, minusTen.callback, minusFifty.callback, minusHundred.callback = plusOneCallback, plusTenCallback, plusFiftyCallback, plusHundredCallback, minusOneCallback, minusTenCallback, minusFiftyCallback, minusHundredCallback
                await ctx.interaction.followup.send(embed = discord.Embed(title = f"You are hacking {u.name}'s Tickets.", color = config.Color.ERROR).set_footer(text = config.footer), view = discord.ui.View(plusOne, plusTen, plusFifty, plusHundred, minusOne, minusTen, minusFifty, minusHundred), ephemeral = True)

            case "Tokens": 
                plusOne     = discord.ui.Button(label = "1️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusTen     = discord.ui.Button(label = "🔟", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusFifty   = discord.ui.Button(label = "5️⃣0️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusHundred = discord.ui.Button(label = "1️⃣0️⃣0️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)

                minusOne     = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusTen     = discord.ui.Button(label = "🔟", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusFifty   = discord.ui.Button(label = "5️⃣0️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusHundred = discord.ui.Button(label = "1️⃣0️⃣0️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)

                async def plusOneCallback(_):     
                    user.tokens += 1
                    user.save()
                async def plusTenCallback(_):     
                    user.tokens += 10
                    user.save()
                async def plusFiftyCallback(_):   
                    user.tokens += 50
                    user.save()
                async def plusHundredCallback(_): 
                    user.tokens += 100
                    user.save()

                async def minusOneCallback(_):     user.tokens -= 1
                async def minusTenCallback(_):     user.tokens -= 10
                async def minusFiftyCallback(_):   user.tokens -= 50
                async def minusHundredCallback(_): user.tokens -= 100

                plusOne.callback, plusTen.callback, plusFifty.callback, plusHundred.callback, minusOne.callback, minusTen.callback, minusFifty.callback, minusHundred.callback = plusOneCallback, plusTenCallback, plusFiftyCallback, plusHundredCallback, minusOneCallback, minusTenCallback, minusFiftyCallback, minusHundredCallback
                await ctx.interaction.followup.send(embed = discord.Embed(title = f"You are hacking {u.name}'s Tokens.", color = config.Color.ERROR).set_footer(text = config.footer), view = discord.ui.View(plusOne, plusTen, plusFifty, plusHundred, minusOne, minusTen, minusFifty, minusHundred), ephemeral = True)

            case "Chips": 
                plusOne     = discord.ui.Button(label = "1️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusTen     = discord.ui.Button(label = "🔟", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusFifty   = discord.ui.Button(label = "5️⃣0️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusHundred = discord.ui.Button(label = "1️⃣0️⃣0️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)

                minusOne     = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusTen     = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusFifty   = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusHundred = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)

                async def plusOneCallback(_):     
                    user.chips += 1
                    user.save()
                async def plusTenCallback(_):     
                    user.chips += 10
                    user.save()
                async def plusFiftyCallback(_):   
                    user.chips += 50
                    user.save()
                async def plusHundredCallback(_): 
                    user.chips += 100
                    user.save()

                async def minusOneCallback(_):     user.chips -= 1
                async def minusTenCallback(_):     user.chips -= 10
                async def minusFiftyCallback(_):   user.chips -= 50
                async def minusHundredCallback(_): user.chips -= 100

                plusOne.callback, plusTen.callback, plusFifty.callback, plusHundred.callback, minusOne.callback, minusTen.callback, minusFifty.callback, minusHundred.callback = plusOneCallback, plusTenCallback, plusFiftyCallback, plusHundredCallback, minusOneCallback, minusTenCallback, minusFiftyCallback, minusHundredCallback
                await ctx.interaction.followup.send(embed = discord.Embed(title = f"You are hacking {u.name}'s Chips.", color = config.Color.ERROR).set_footer(text = config.footer), view = discord.ui.View(plusOne, plusTen, plusFifty, plusHundred, minusOne, minusTen, minusFifty, minusHundred), ephemeral = True)

            case "Dice": 
                plusOne     = discord.ui.Button(label = "1️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusTen     = discord.ui.Button(label = "🔟", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusFifty   = discord.ui.Button(label = "5️⃣0️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusHundred = discord.ui.Button(label = "1️⃣0️⃣0️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)

                minusOne     = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusTen     = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusFifty   = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusHundred = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)

                async def plusOneCallback(_):     
                    user.dice += 1
                    user.save()
                async def plusTenCallback(_):     
                    user.dice += 10
                    user.save()
                async def plusFiftyCallback(_):   
                    user.dice += 50
                    user.save()
                async def plusHundredCallback(_): 
                    user.dice += 100
                    user.save()

                async def minusOneCallback(_):     user.dice -= 1
                async def minusTenCallback(_):     user.dice -= 10
                async def minusFiftyCallback(_):   user.dice -= 50
                async def minusHundredCallback(_): user.dice -= 100

                plusOne.callback, plusTen.callback, plusFifty.callback, plusHundred.callback, minusOne.callback, minusTen.callback, minusFifty.callback, minusHundred.callback = plusOneCallback, plusTenCallback, plusFiftyCallback, plusHundredCallback, minusOneCallback, minusTenCallback, minusFiftyCallback, minusHundredCallback
                await ctx.interaction.followup.send(embed = discord.Embed(title = f"You are hacking {u.name}'s Dice.", color = config.Color.ERROR).set_footer(text = config.footer), view = discord.ui.View(plusOne, plusTen, plusFifty, plusHundred, minusOne, minusTen, minusFifty, minusHundred), ephemeral = True)

            case "Dominoes": 
                plusOne     = discord.ui.Button(label = "1️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusTen     = discord.ui.Button(label = "🔟", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusFifty   = discord.ui.Button(label = "5️⃣0️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusHundred = discord.ui.Button(label = "1️⃣0️⃣0️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)

                minusOne     = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusTen     = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusFifty   = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusHundred = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)

                async def plusOneCallback(_):     
                    user.dominoes += 1
                    user.save()
                async def plusTenCallback(_):     
                    user.dominoes += 10
                    user.save()
                async def plusFiftyCallback(_):   
                    user.dominoes += 50
                    user.save()
                async def plusHundredCallback(_): 
                    user.dominoes += 100
                    user.save()

                async def minusOneCallback(_):     user.dominoes -= 1
                async def minusTenCallback(_):     user.dominoes -= 10
                async def minusFiftyCallback(_):   user.dominoes -= 50
                async def minusHundredCallback(_): user.dominoes -= 100

                plusOne.callback, plusTen.callback, plusFifty.callback, plusHundred.callback, minusOne.callback, minusTen.callback, minusFifty.callback, minusHundred.callback = plusOneCallback, plusTenCallback, plusFiftyCallback, plusHundredCallback, minusOneCallback, minusTenCallback, minusFiftyCallback, minusHundredCallback
                await ctx.interaction.followup.send(embed = discord.Embed(title = f"You are hacking {u.name}'s Dominoes.", color = config.Color.ERROR).set_footer(text = config.footer), view = discord.ui.View(plusOne, plusTen, plusFifty, plusHundred, minusOne, minusTen, minusFifty, minusHundred), ephemeral = True)

            case "Tiles": 
                plusOne     = discord.ui.Button(label = "1️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusTen     = discord.ui.Button(label = "🔟", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusFifty   = discord.ui.Button(label = "5️⃣0️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusHundred = discord.ui.Button(label = "1️⃣0️⃣0️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)

                minusOne     = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusTen     = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusFifty   = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusHundred = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)

                async def plusOneCallback(_):     
                    user.tiles += 1
                    user.save()
                async def plusTenCallback(_):     
                    user.tiles += 10
                    user.save()
                async def plusFiftyCallback(_):   
                    user.tiles += 50
                    user.save()
                async def plusHundredCallback(_): 
                    user.tiles += 100
                    user.save()

                async def minusOneCallback(_):     user.tiles -= 1
                async def minusTenCallback(_):     user.tiles -= 10
                async def minusFiftyCallback(_):   user.tiles -= 50
                async def minusHundredCallback(_): user.tiles -= 100

                plusOne.callback, plusTen.callback, plusFifty.callback, plusHundred.callback, minusOne.callback, minusTen.callback, minusFifty.callback, minusHundred.callback = plusOneCallback, plusTenCallback, plusFiftyCallback, plusHundredCallback, minusOneCallback, minusTenCallback, minusFiftyCallback, minusHundredCallback
                await ctx.interaction.followup.send(embed = discord.Embed(title = f"You are hacking {u.name}'s Tiles.", color = config.Color.ERROR).set_footer(text = config.footer), view = discord.ui.View(plusOne, plusTen, plusFifty, plusHundred, minusOne, minusTen, minusFifty, minusHundred), ephemeral = True)

            case "Chits": 
                plusOne     = discord.ui.Button(label = "1️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusTen     = discord.ui.Button(label = "🔟", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusFifty   = discord.ui.Button(label = "5️⃣0️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusHundred = discord.ui.Button(label = "1️⃣0️⃣0️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)

                minusOne     = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusTen     = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusFifty   = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusHundred = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)

                async def plusOneCallback(_):     
                    user.chits += 1
                    user.save()
                async def plusTenCallback(_):     
                    user.chits += 10
                    user.save()
                async def plusFiftyCallback(_):   
                    user.chits += 50
                    user.save()
                async def plusHundredCallback(_): 
                    user.chits += 100
                    user.save()

                async def minusOneCallback(_):     user.chits -= 1
                async def minusTenCallback(_):     user.chits -= 10
                async def minusFiftyCallback(_):   user.chits -= 50
                async def minusHundredCallback(_): user.chits -= 100

                plusOne.callback, plusTen.callback, plusFifty.callback, plusHundred.callback, minusOne.callback, minusTen.callback, minusFifty.callback, minusHundred.callback = plusOneCallback, plusTenCallback, plusFiftyCallback, plusHundredCallback, minusOneCallback, minusTenCallback, minusFiftyCallback, minusHundredCallback
                await ctx.interaction.followup.send(embed = discord.Embed(title = f"You are hacking {u.name}'s Chits.", color = config.Color.ERROR).set_footer(text = config.footer), view = discord.ui.View(plusOne, plusTen, plusFifty, plusHundred, minusOne, minusTen, minusFifty, minusHundred), ephemeral = True)

            case "Experience": 
                plusOne     = discord.ui.Button(label = "1️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusTen     = discord.ui.Button(label = "🔟", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusFifty   = discord.ui.Button(label = "5️⃣0️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusHundred = discord.ui.Button(label = "1️⃣0️⃣0️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)

                minusOne     = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusTen     = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusFifty   = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusHundred = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)

                async def plusOneCallback(_):     
                    user.xp += 1
                    user.save()
                async def plusTenCallback(_):     
                    user.xp += 10
                    user.save()
                async def plusFiftyCallback(_):   
                    user.xp += 50
                    user.save()
                async def plusHundredCallback(_): 
                    user.xp += 100
                    user.save()

                async def minusOneCallback(_):     user.xp -= 1
                async def minusTenCallback(_):     user.xp -= 10
                async def minusFiftyCallback(_):   user.xp -= 50
                async def minusHundredCallback(_): user.xp -= 100

                plusOne.callback, plusTen.callback, plusFifty.callback, plusHundred.callback, minusOne.callback, minusTen.callback, minusFifty.callback, minusHundred.callback = plusOneCallback, plusTenCallback, plusFiftyCallback, plusHundredCallback, minusOneCallback, minusTenCallback, minusFiftyCallback, minusHundredCallback
                await ctx.interaction.followup.send(embed = discord.Embed(title = f"You are hacking {u.name}'s Experience.", color = config.Color.ERROR).set_footer(text = config.footer), view = discord.ui.View(plusOne, plusTen, plusFifty, plusHundred, minusOne, minusTen, minusFifty, minusHundred), ephemeral = True)

            case "Turing":
                select = discord.ui.Select(placeholder = "Turing to give/remove", options = [
                    discord.SelectOption(label = "Chess", value = "chess"),
                    discord.SelectOption(label = "Checkers", value = "checkers"),
                    discord.SelectOption(label = "Trust", value = "trust"),
                    discord.SelectOption(label = "BAMBOOZLE!", value = "bamboozle"),
                    discord.SelectOption(label = "White on Black", value = "wob"),
                    discord.SelectOption(label = "Hold 'Em", value = "holdem")
                ])

                async def selectCallback(_):
                    match select.values:
                        case "chess": 
                            if "chess" in user.turing: user.turing.remove("chess")
                            else: user.turing.append("chess")
                        
                        case "checkers": 
                            if "checkers" in user.turing: user.turing.remove("checkers")
                            else: user.turing.append("checkers")

                        case "trust": 
                            if "trust" in user.turing: user.turing.remove("trust")
                            else: user.turing.append("trust")

                        case "bamboozle": 
                            if "bamboozle" in user.turing: user.turing.remove("bamboozle")
                            else: user.turing.append("bamboozle")

                        case "wob": 
                            if "wob" in user.turing: user.turing.remove("wob")
                            else: user.turing.append("wob")

                        case "holdem": 
                            if "holdem" in user.turing: user.turing.remove("holdem")
                            else: user.turing.append("holdem")

                        case _: await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.GENERIC.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)

                select.callback = selectCallback
                await ctx.interaction.followup.send(embed = discord.Embed(title = f"You are hacking {u.name}'s Turing Access.", color = config.Color.ERROR).set_footer(text = config.footer), view = discord.ui.View(select), ephemeral = True)

            case "Achievements":
                message: discord.Message = None
                select = discord.ui.Select(placeholder = "Where to change achievments from...", options = [
                    discord.SelectOption(label = "General", value = "theadas"),
                ])

                async def selectCallback(interaction):
                    match select.values[0]:
                        case "theadas":
                            s = discord.ui.Select(placeholder = "Where to change achievments from...", options = [
                                discord.SelectOption(label = "Contributor", value = "contributor"),
                            ])

                            async def sCallback(_):
                                match s.values:
                                    case "contributor": 
                                        if "contributor" in user.achievements["theadas"]: user.achievements["theadas"].remove("contributor")
                                        else: user.achievements["theadas"].append("contributor")

                                    case _: await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.GENERIC.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                            
                            s.callback = sCallback
                            await message.edit(embed = discord.Embed(title = f"You are hacking {u.name}'s Achievements.", color = config.Color.ERROR).set_footer(text = config.footer), view = discord.ui.View(s), ephemeral = True)

                select.callback = selectCallback
                message = await ctx.interaction.followup.send(embed = discord.Embed(title = f"You are hacking {u.name}'s Achievements.", color = config.Color.ERROR).set_footer(text = config.footer), view = discord.ui.View(select), ephemeral = True)

            case "Priority": 
                await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer, ephemeral = True), ephemeral = True)
                return

            case "Backgrounds": 
                await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer, ephemeral = True), ephemeral = True)
                return

            case "BAMBOOZLE!": 
                await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer, ephemeral = True), ephemeral = True)
                return

            case "Checkers": 
                await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer, ephemeral = True), ephemeral = True)
                return

            case "Chess": 
                await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer, ephemeral = True), ephemeral = True)
                return

            case "Gridlock": 
                await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer, ephemeral = True), ephemeral = True)
                return

            case "2048": 
                plusOne     = discord.ui.Button(label = "1️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusTen     = discord.ui.Button(label = "🔟", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusFifty   = discord.ui.Button(label = "5️⃣0️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusHundred = discord.ui.Button(label = "1️⃣0️⃣0️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)

                minusOne     = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusTen     = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusFifty   = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusHundred = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)

                async def plusOneCallback(_):     
                    user.plays["2048"] += 1
                    user.save()

                async def plusTenCallback(_):     
                    user.plays["2048"] += 10
                    user.save()

                async def plusFiftyCallback(_):   
                    user.plays["2048"] += 50
                    user.save()

                async def plusHundredCallback(_): 
                    user.plays["2048"] += 100
                    user.save()


                async def minusOneCallback(_):     user.plays["2048"] -= 1
                async def minusTenCallback(_):     user.plays["2048"] -= 10
                async def minusFiftyCallback(_):   user.plays["2048"] -= 50
                async def minusHundredCallback(_): user.plays["2048"] -= 100

                plusOne.callback, plusTen.callback, plusFifty.callback, plusHundred.callback, minusOne.callback, minusTen.callback, minusFifty.callback, minusHundred.callback = plusOneCallback, plusTenCallback, plusFiftyCallback, plusHundredCallback, minusOneCallback, minusTenCallback, minusFiftyCallback, minusHundredCallback
                await ctx.interaction.followup.send(embed = discord.Embed(title = f"You are hacking {u.name}'s 2048 Plays.", color = config.Color.ERROR).set_footer(text = config.footer), view = discord.ui.View(plusOne, plusTen, plusFifty, plusHundred, minusOne, minusTen, minusFifty, minusHundred), ephemeral = True)

            case "Hangman": 
                plusOne     = discord.ui.Button(label = "1️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusTen     = discord.ui.Button(label = "🔟", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusFifty   = discord.ui.Button(label = "5️⃣0️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)
                plusHundred = discord.ui.Button(label = "1️⃣0️⃣0️⃣", emoji = "➕", style = discord.ButtonStyle.secondary, row = 0)

                minusOne     = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusTen     = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusFifty   = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)
                minusHundred = discord.ui.Button(label = "1️⃣", emoji = "➖", style = discord.ButtonStyle.secondary, row = 1)

                async def plusOneCallback(_):     
                    user.plays["hangman"] += 1
                    user.save()

                async def plusTenCallback(_):     
                    user.plays["hangman"] += 10
                    user.save()

                async def plusFiftyCallback(_):   
                    user.plays["hangman"] += 50
                    user.save()

                async def plusHundredCallback(_): 
                    user.plays["hangman"] += 100
                    user.save()


                async def minusOneCallback(_):     user.plays["hangman"] -= 1
                async def minusTenCallback(_):     user.plays["hangman"] -= 10
                async def minusFiftyCallback(_):   user.plays["hangman"] -= 50
                async def minusHundredCallback(_): user.plays["hangman"] -= 100

                plusOne.callback, plusTen.callback, plusFifty.callback, plusHundred.callback, minusOne.callback, minusTen.callback, minusFifty.callback, minusHundred.callback = plusOneCallback, plusTenCallback, plusFiftyCallback, plusHundredCallback, minusOneCallback, minusTenCallback, minusFiftyCallback, minusHundredCallback
                await ctx.interaction.followup.send(embed = discord.Embed(title = f"You are hacking {u.name}'s Hangman Plays.", color = config.Color.ERROR).set_footer(text = config.footer), view = discord.ui.View(plusOne, plusTen, plusFifty, plusHundred, minusOne, minusTen, minusFifty, minusHundred), ephemeral = True)

            case "Game Purge": pickle.dump(None, open(f"{os.path.join(os.path.dirname(__file__), 'data/games')}/{user.id}.p", "wb"))

            case _: 
                await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.GENERIC.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                return
    else: await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.PERMISSION.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)

# pyright: reportInvalidTypeForm=false
@bot.slash_command(name = "profile", description = "View a user's profile.")
async def profileCommand(ctx, user: discord.Option(discord.Member, "Leave blank to check your own.") = None, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)
    if ctx.author.bot: return
    
    if user is None: user = ctx.author
    u: User = User(user.id)

    moreSelect = discord.ui.Select(placeholder = "See More...", options = [
        discord.SelectOption(label = "Titles", value = "titles"),
        discord.SelectOption(label = "Backgrounds", value = "backgrounds"),
        discord.SelectOption(label = "Holo Cards", value = "holos"),
        discord.SelectOption(label = "WOB Packs", value = "whiteonblack"),
        discord.SelectOption(label = "Trust Variants", value = "trust"),
        discord.SelectOption(label = "Achievements", value = "achievements"),
        discord.SelectOption(label = "Medals", value = "medals")
    ])

    changeSelect = discord.ui.Select(placeholder = "Change Your...")
    if len(u.titles) > 1: changeSelect.add_option(label = "Title", value = "title")
    if len(u.backgrounds) > 1: changeSelect.add_option(label = "Profile Background", value = "background")

    async def moreCallback(interaction):
        await interaction.response.defer(ephemeral = True)

        match moreSelect.values[0]:
            case "titles": 
                str = ""
                for i in u.titles: str += f"\n- {i}"
                if len(str) == 0: str = "None"

                await interaction.followup.send(embed = discord.Embed(title = "Titles:", description = str, color = config.Color.COLORLESS).set_footer(text = config.footer), ephemeral = not show)
            
            case "backgrounds": 
                await interaction.followup.send(embed = discord.Embed(title = "Backgrounds:", description = "None", color = config.Color.COLORLESS).set_footer(text = config.footer), ephemeral = not show)
            
            case "holos": 
                await interaction.followup.send(embed = discord.Embed(title = "Holo Arts:", description = "None", color = config.Color.COLORLESS).set_footer(text = config.footer), ephemeral = not show)
            
            case "whiteonblack": 
                str = ""
                for i in u.expansions: str += f"\n- {i.value}"
                if len(str) == 0: str = "None"

                await interaction.followup.send(embed = discord.Embed(title = "White on Black packs:", description = str, color = config.Color.COLORLESS).set_footer(text = config.footer), ephemeral = not show)
            
            case "trust": 
                str = ""
                for i in u.variants: str += f"\n- {i.value}"
                if len(str) == 0: str = "None"

                await interaction.followup.send(embed = discord.Embed(title = "Trust Variants:", description = str, color = config.Color.COLORLESS).set_footer(text = config.footer), ephemeral = not show)
            
            case "achievements": 
                e = discord.Embed(title = "Achievements:", description = u.achievement_str("theadas"), color = config.Color.COLORLESS).set_footer(text = config.footer)
                
                if u.achievement_str("bamboozle") != "None": e.add_field(name = "BAMBOOZLE!", value = u.achievement_str("bamboozle"), inline = False)
                if u.achievement_str("whiteonblack") != "None": e.add_field(name = "White on Black", value = u.achievement_str("whiteonblack"), inline = False)
                if u.achievement_str("checkers") != "None": e.add_field(name = "Checkers", value = u.achievement_str("checkers"), inline = False)
                if u.achievement_str("chess") != "None": e.add_field(name = "Chess", value = u.achievement_str("chess"), inline = False)
                if u.achievement_str("gridlock") != "None": e.add_field(name = "Gridlock", value = u.achievement_str("gridlock"), inline = False)
                if u.achievement_str("trust") != "None": e.add_field(name = "Trust", value = u.achievement_str("trust"), inline = False)

                await interaction.followup.send(embed = e, ephemeral = not show)
            case "medals":
                e = discord.Embed(title = "Medals:", color = config.Color.COLORLESS).set_footer(text = config.footer)

                if u.stats["bamboozle"]["wins"] + u.stats["bamboozle"]["losses"] > 0: e.add_field(name = "BAMBOOZLE", value = f"```Manipulator: {u.stats['bamboozle']['medals']['manipulator']}\nPoker Face: {u.stats['bamboozle']['medals']['poker face']}\nBackstabber: {u.stats['bamboozle']['medals']['backstabber']}```", inline = False)
                if u.stats["whiteonblack"]["games"] > 0: e.add_field(name = "White on Black", value = f"```Lucky: {u.stats['whiteonblack']['medals']['lucky']}\nFunny: {u.stats['whiteonblack']['medals']['funny']}\nNasty: {u.stats['whiteonblack']['medals']['nasty']}\nOffensive: {u.stats['whiteonblack']['medals']['offensive']}```", inline = False)
                if u.stats["checkers"]["wins"] + u.stats["checkers"]["losses"] > 0: e.add_field(name = "Checkers", value = f"```Played Well: {u.stats['checkers']['medals']['played well']}```", inline = False)
                if u.stats["chess"]["wins"] + u.stats["chess"]["losses"] > 0: e.add_field(name = "Chess", value = f"```Knowledgeable: {u.stats['chess']['medals']['knowledgeable']}\nRisk Taker: {u.stats['chess']['medals']['risk taker']}\nPlayed fast: {u.stats['chess']['medals']['played Fast']}```", inline = False)
                if u.stats["gridlock"]["wins"] + u.stats["gridlock"]["losses"] > 0: e.add_field(name = "Gridlock", value = f"```Interesting Deck: {u.stats['gridlock']['medals']['interesting deck']}\nPlayed Well: {u.stats['gridlock']['medals']['played well']}\nPlayed Fast: {u.stats['gridlock']['medals']['played fast']}```", inline = False)
                if u.stats["trust"]["wins"] + u.stats["trust"]["losses"] > 0: e.add_field(name = "Trust", value = f"```Lucky: {u.stats['trust']['medals']['lucky']}\nSmart Investor: {u.stats['trust']['medals']['smart investor']}\nNegotiator: {u.stats['trust']['medals']['negotiator']}```", inline = False)
                if len(e.fields) == 0: e.description = "None"

                await interaction.followup.send(embed = e, ephemeral = not show)
            
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
    if u.stats["bamboozle"]["wins"] + u.stats["bamboozle"]["losses"] > 0: embed.add_field(name = "BAMBOOZLE!", value = f"Skill Rating (SR): {math.floor(u.sr['bamboozle'])}\nGames Played: {u.stats['bamboozle']['wins'] + u.stats['bamboozle']['losses']}\nGames Won: {u.stats['bamboozle']['wins']} ({math.floor(u.stats['bamboozle']['wins'] / (u.stats['bamboozle']['wins'] + u.stats['bamboozle']['losses'])) * 100})% Winrate\nHolo Cards Owned: {bamboozle_holos}\n\nAchievements: {u.achievement_str('bamboozle')}", inline = False)
    if u.stats["blackjack"]["wins"] + u.stats["blackjack"]["losses"] > 0: embed.add_field(name = "Blackjack",  value = f"Games Played: {u.stats['blackjack']['wins'] + u.stats['blackjack']['losses']}\n\nAchievements: {u.achievement_str('blackjack')}", inline = False)
    if u.stats["whiteonblack"]["games"] > 0: embed.add_field(name = "White on Black",  value = f"Games Played: {u.stats['whiteonblack']['games']}\n\nExpansions Owned: {expansion_str}\nAchievements: {u.achievement_str('whiteonblack')}", inline = False)
    if u.stats["checkers"]["wins"] + u.stats["checkers"]["losses"] > 0: embed.add_field(name = "Checkers",  value = f"Skill Rating (SR): {math.floor(u.sr['checkers'])}\nGames Played: {u.stats['checkers']['wins'] + u.stats['checkers']['losses']}\nGames Won: {u.stats['checkers']['wins']} ({math.floor(u.stats['checkers']['wins'] / (u.stats['checkers']['wins'] + u.stats['checkers']['losses'])) * 100})% Winrate\n\nAchievements: {u.achievement_str('checkers')}", inline = False)
    if u.stats["chess"]["wins"] + u.stats["chess"]["losses"] > 0: embed.add_field(name = "Chess",  value = f"Skill Rating (SR): {math.floor(u.sr['chess'])}\nGames Played: {u.stats['chess']['wins'] + u.stats['chess']['losses']}\nGames Won: {u.stats['chess']['wins']} ({math.floor(u.stats['chess']['wins'] / (u.stats['chess']['wins'] + u.stats['chess']['losses'])) * 100})% Winrate\n\nAchievements: {u.achievement_str('chess')}", inline = False)
    if u.stats["gridlock"]["wins"] + u.stats["gridlock"]["losses"] > 0: embed.add_field(name = "Gridlock",  value = f"Skill Rating (SR): {math.floor(u.sr['gridlock'])}\nGames Played: {u.stats['gridlock']['wins'] + u.stats['gridlock']['losses']}\nGames Won: {u.stats['gridlock']['wins']} ({math.floor(u.stats['gridlock']['wins'] / (u.stats['gridlock']['wins'] + u.stats['gridlock']['losses'])) * 100})% Winrate\nHolo Cards Owned: {gridlock_holos}\n**Packs:** {u.packs[gridlock.Pack.SMALL]} Small, {u.packs[gridlock.Pack.LARGE]} Large, {u.packs[gridlock.Pack.PREMIUM]} Premium\n\nAchievements: {u.achievement_str('gridlock')}", inline = False)
    if u.stats["hangman"]["wins"] + u.stats["hangman"]["losses"] > 0: embed.add_field(name = "Hangman",  value = f"Games Played: {u.stats['hangman']['wins'] + u.stats['hangman']['losses']}\n\nGames Won: {u.stats['hangman']['wins']} ({math.floor(u.stats['hangman']['wins'] / (u.stats['hangman']['wins'] + u.stats['hangman']['losses'])) * 100})% Winrate\n\nAchievements: {u.achievement_str('hangman')}", inline = False)
    if u.stats["trust"]["wins"] + u.stats["trust"]["losses"] > 0: embed.add_field(name = "trust",  value = f"Games Played: {u.stats['trust']['wins'] + u.stats['trust']['losses']}\nGames Won: {u.stats['trust']['wins']} ({math.floor(u.stats['trust']['wins'] / (u.stats['trust']['wins'] + u.stats['trust']['losses'])) * 100})% Winrate\n\nVariants Owned: {variant_str}\nAchievements: {u.achievement_str('trust')}", inline = False)
    if u.stats["rps"]["wins"] + u.stats["rps"]["losses"] > 0: embed.add_field(name = "Rock Paper Scissors",  value = f"Games Played: {u.stats['rps']['wins'] + u.stats['rps']['losses']}\n\nGames Won: {u.stats['rps']['wins']} ({math.floor(u.stats['rps']['wins'] / (u.stats['rps']['wins'] + u.stats['rps']['losses'])) * 100})% Winrate\n\nAchievements: {u.achievement_str('rps')}", inline = False)
    if u.stats["slots"]["wins"] + u.stats["slots"]["losses"] > 0: embed.add_field(name = "Blackjack",  value = f"Games Played: {u.stats['slots']['wins'] + u.stats['slots']['losses']}\n\nAchievements: {u.achievement_str('slots')}", inline = False)
    if u.stats["tictactoe"]["wins"] + u.stats["tictactoe"]["losses"] > 0: embed.add_field(name = "Tic Tac Toe",  value = f"Games Played: {u.stats['tictactoe']['wins'] + u.stats['tictactoe']['losses']}\n\nGames Won: {u.stats['tictactoe']['wins']} ({math.floor(u.stats['tictactoe']['wins'] / (u.stats['tictactoe']['wins'] + u.stats['tictactoe']['losses'])) * 100})% Winrate\n\nAchievements: {u.achievement_str('tictactoe')}", inline = False)

    await ctx.interaction.followup.send(embed = embed, view = view)

@bot.slash_command(name = "shop", description = "Turn your currency into shiny new toys!")
async def shopCommand(ctx):
    await ctx.defer(ephemeral = True)
    if ctx.author.bot: return

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
            Page(embeds = [discord.Embed(title = "Domino Shop",   description = "**White on Black Packs:** Coming soon!\n**Trust Variants:** Coming soon!", color = config.Color.COLORLESS).set_footer(text = config.footer)], custom_view = dominoView),
            Page(embeds = [discord.Embed(title = "Tile Shop",     description = "**Profile Backgrounds:** Coming soon!\n**Holo Arts:** Coming soon!", color = config.Color.COLORLESS).set_footer(text = config.footer)], custom_view = tileView),
            Page(embeds = [discord.Embed(title = "Chit Shop",     description = "**x2 Medals:** 3 Chits\n## Turing (play vs. cpu)\n**Chess:** Coming soon!\n**Checkers:** Coming soon!\n**Trust:** Coming soon!\n**BAMBOOZLE!:** Coming soon!\n## Strategy Guides:\n**Chess:** Coming soon!\n**Checkers:** Coming soon!\n**Gridlock:** Coming soon!", color = config.Color.COLORLESS).set_footer(text = config.footer)], custom_view = chitView)
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
    if ctx.author.bot: return
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

@bot.slash_command(name = "help", description = "Learn how to use my commands!")
async def helpCommand(ctx, category: discord.Option(str, "pick a command or game to get help with") = None, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)
    if ctx.author.bot: return

    if not category:
        default:  List[discord.Embed] = [discord.Embed(title = "Theadas Help", description = "Below is a list of my games and commands along with their descriptions. For more details or usage for one game or command, use /help <category> where category is the game or command.", color = config.Color.COLORLESS)]
        commands: List[discord.Embed] = [discord.Embed(title = "Commands", color = config.Color.COLORLESS)]
        games:    List[discord.Embed] = [discord.Embed(title = "Games",    color = config.Color.COLORLESS)]
        n: int = 0

        for i in bot.application_commands:
            if n >= 25: commands.append(discord.Embed(color = config.Color.COLORLESS))
            commands[-1].add_field(name = i.name, value = i.description if i.description else i.name)
            n += 1
        
        n = 0
        for i in _games: 
            if n >= 25: games.append(discord.Embed(color = config.Color.COLORLESS))
            games[-1].add_field(name = i.name, value = i.description if i.description else i.name)
            n += 1

        for i in commands: default.append(i)
        for i in games:    default.append(i)
        default.append(discord.Embed(description = config.footer, color = config.Color.COLORLESS))

        await ctx.interaction.followup.send(embeds = default)
        return

    match category.lower():
        # COMMANDS
        case "ping": ctx.interaction.followup.send(embed = discord.Embed(title = "Ping Command", description = "Test the bot's response time.\n**Usage:** /ping", color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "profile": ctx.interaction.followup.send(embed = discord.Embed(title = "Profile Command", description = "View a user's profile. If you do not specify a user, your own will be shown.\n**Usage:** /profile [user]", color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "leaderboard": ctx.interaction.followup.send(embed = discord.Embed(title = "Leaderboard Command", description = "See how you stack up against other server members!\n**Usage:** /leaderboard", color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "board": ctx.interaction.followup.send(embed = discord.Embed(title = "Leaderboard Command", description = "See how you stack up against other server members!\n**Usage:** /leaderboard", color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "credits": ctx.interaction.followup.send(embed = discord.Embed(title = "Credits Command", description = "\n**Usage:** /credits", color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "shop": ctx.interaction.followup.send(embed = discord.Embed(title = "Shop Command", description = "\n**Usage:** /shop [category]", color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "support": ctx.interaction.followup.send(embed = discord.Embed(title = "Support Command", description = "\n**Usage:** /support", color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "play": ctx.interaction.followup.send(embed = discord.Embed(title = "Play Command", description = "\n**Usage:** /play <game>", color = config.Color.COLORLESS).set_footer(text = config.footer))
        
        # GAMES
        case "bamboozle": ctx.interaction.followup.send(discord.Embed(title = "BAMBOOZLE!", description = bamboozle.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "boozle": ctx.interaction.followup.send(discord.Embed(title = "BAMBOOZLE!", description = bamboozle.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "blackjack": ctx.interaction.followup.send(discord.Embed(title = "Blackjack", description = blackjack.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "bj": ctx.interaction.followup.send(discord.Embed(title = "Blackjack", description = blackjack.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "whiteonblack": ctx.interaction.followup.send(discord.Embed(title = "White on Black", description = whiteonblack.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "white on black": ctx.interaction.followup.send(discord.Embed(title = "White on Black", description = whiteonblack.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "wob": ctx.interaction.followup.send(discord.Embed(title = "White on Black", description = whiteonblack.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "cah": ctx.interaction.followup.send(discord.Embed(title = "White on Black", description = whiteonblack.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "checkers": ctx.interaction.followup.send(discord.Embed(title = "Checkers", description = checkers.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "chess": ctx.interaction.followup.send(discord.Embed(title = "Chess", description = chess.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "gridlock": ctx.interaction.followup.send(discord.Embed(title = "Gridlock", description = gridlock.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "gridlocktcg": ctx.interaction.followup.send(discord.Embed(title = "Gridlock", description = gridlock.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "gridlock tcg": ctx.interaction.followup.send(discord.Embed(title = "Gridlock", description = gridlock.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "tcg": ctx.interaction.followup.send(discord.Embed(title = "Gridlock", description = gridlock.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "hangman": ctx.interaction.followup.send(discord.Embed(title = "Hangman", description = hangman.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "holdem": ctx.interaction.followup.send(discord.Embed(title = "Holdem", description = holdem.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "hold em": ctx.interaction.followup.send(discord.Embed(title = "Holdem", description = holdem.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "hold 'em": ctx.interaction.followup.send(discord.Embed(title = "Holdem", description = holdem.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "trust": ctx.interaction.followup.send(discord.Embed(title = "trust", description = trust.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "rockpaperscissors": ctx.interaction.followup.send(discord.Embed(title = "Rock Paper Scissors", description = rps.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "rps": ctx.interaction.followup.send(discord.Embed(title = "Rock Paper Scissors", description = rps.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "slots": ctx.interaction.followup.send(discord.Embed(title = "Slots", description = slots.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "tactactoe": ctx.interaction.followup.send(discord.Embed(title = "Tic Tac Toe", description = tictactoe.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "twentyfortyeight": ctx.interaction.followup.send(discord.Embed(title = '2048', description = twentyfortyeight.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "twenty forty eight": ctx.interaction.followup.send(discord.Embed(title = '2048', description = twentyfortyeight.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        case "2048": ctx.interaction.followup.send(discord.Embed(title = '2048', description = twentyfortyeight.description, color = config.Color.COLORLESS).set_footer(text = config.footer))
        
        # DEFAULT
        case _: 
            default:  List[discord.Embed] = [discord.Embed(title = "Theadas Help", description = "Below is a list of my games and commands along with their descriptions. For more details or usage for one game or command, use /help <category> where category is the game or command.", color = config.Color.COLORLESS)]
            commands: List[discord.Embed] = [discord.Embed(title = "Commands", color = config.Color.COLORLESS)]
            games:    List[discord.Embed] = [discord.Embed(title = "Games",    color = config.Color.COLORLESS)]
            n: int = 0

            for i in bot.application_commands:
                if n >= 25: commands.append(discord.Embed(color = config.Color.COLORLESS))
                commands[-1].add_field(name = i.name, value = i.description if i.description else i.name, color = config.Color.COLORLESS)
                n += 1
            
            n = 0
            for i in _games: 
                if n >= 25: games.append(discord.Embed(color = config.Color.COLORLESS))
                games[-1].add_field(name = i.name, value = i.description if i.description else i.name, color = config.Color.COLORLESS)
                n += 1

            for i in commands: default.append(i)
            for i in games:    default.append(i)

            await ctx.interaction.followup.send(embeds = default)

@bot.slash_command(name = "leaderboard", description = "See how you stack up against other server members!")
async def leaderboardCommand(ctx, page: discord.Option(int, "20 users on each page") = 1, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)
    if ctx.author.bot: return

    board = ""
    n = page

    ids = [u.id async for u in ctx.guild.fetch_members() if not u.bot]
    for i in sorted([User(i) for i in ids], key = lambda x: x.xp, reverse = True)[0 + (20 * (page - 1)) : 20 * page]: 
        name = await bot.fetch_user(i.id)
        name = name.name
        xp = ""
        
        for x in range(10): xp += "▰" if x < round((i.xp / i.get_next_level()) * 10) else "▱"
        board += f"\n[{n}] ‣ **{name} (Level {i.get_level()}):** {i.xp} xp `{xp}`"
        n += 1
    
    await ctx.interaction.followup.send(embed = discord.Embed(title = f"{ctx.guild.name} Leaderboard", description = board, color = config.Color.COLORLESS).set_footer(text = f"Version: {config.version}"))

@bot.slash_command(name = "credits", description = "A lot of cool people are behind this project!")
async def creditsCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)
    if ctx.author.bot: return

    str = ""

    for i in config.credits.keys(): str += f"{i}: {config.credits[i]}\n"
    embed = discord.Embed(title = "Contributors:", description = str, color = config.Color.COLORLESS).set_footer(text = f"Version: {config.version}")
    await ctx.interaction.followup.send(embed = embed)
    
@bot.slash_command(name = "support", description = "Need a hand?")
async def supportCommand(ctx, show: discord.Option(bool, "Select false to keep the response private.") = False):
    await ctx.defer(ephemeral = not show)
    if ctx.author.bot: return

    embed = discord.Embed(title = "Support", description = "Use `/help` to learn how to use my commands or `/info` to learn about my games. If you need further support, have suggestions, or want to report a bug, join our support server:", color = config.Color.COLORLESS).set_footer(text = config.footer).set_thumbnail(url = "https://cdn.discordapp.com/icons/1101982625003995270/a_ee9d87e8365151c5940a2de8aea51c06.webp")
    await ctx.interaction.followup.send(view = discord.ui.View(discord.ui.Button(label = "Join", url = "https://discord.gg/CfPYvDZ6rF", style = discord.ButtonStyle.success)), embed = embed)

# TODO: user commands
@bot.user_command(name="View Profile")
async def profileUserCommand(ctx, user: discord.Member):
    await ctx.defer(ephemeral = True)
    if ctx.author.bot: return

    if user is None: user = ctx.author
    u: User = User(user.id)

    moreSelect = discord.ui.Select(placeholder = "See More...", options = [
        discord.SelectOption(label = "Titles", value = "titles"),
        discord.SelectOption(label = "Backgrounds", value = "backgrounds"),
        discord.SelectOption(label = "Holo Cards", value = "holos"),
        discord.SelectOption(label = "WOB Packs", value = "whiteonblack"),
        discord.SelectOption(label = "Trust Variants", value = "trust"),
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
            case "trust": pass
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
    if u.stats["bamboozle"]["wins"] + u.stats["bamboozle"]["losses"] > 0: embed.add_field(name = "BAMBOOZLE!", value = f"Skill Rating (SR): {math.floor(u.sr['bamboozle'])}\nGames Played: {u.stats['bamboozle']['wins'] + u.stats['bamboozle']['losses']}\nGames Won: {u.stats['bamboozle']['wins']} ({math.floor(u.stats['bamboozle']['wins'] / (u.stats['bamboozle']['wins'] + u.stats['bamboozle']['losses'])) * 100})% Winrate\nHolo Cards Owned: {bamboozle_holos}\n\nAchievements: {u.achievement_str('bamboozle')}", inline = False)
    if u.stats["blackjack"]["wins"] + u.stats["blackjack"]["losses"] > 0: embed.add_field(name = "Blackjack",  value = f"Games Played: {u.stats['blackjack']['wins'] + u.stats['blackjack']['losses']}\n\nAchievements: {u.achievement_str('blackjack')}", inline = False)
    if u.stats["whiteonblack"]["games"] > 0: embed.add_field(name = "White on Black",  value = f"Games Played: {u.stats['whiteonblack']['games']}\n\nExpansions Owned: {expansion_str}\nAchievements: {u.achievement_str('whiteonblack')}", inline = False)
    if u.stats["checkers"]["wins"] + u.stats["checkers"]["losses"] > 0: embed.add_field(name = "Checkers",  value = f"Skill Rating (SR): {math.floor(u.sr['checkers'])}\nGames Played: {u.stats['checkers']['wins'] + u.stats['checkers']['losses']}\nGames Won: {u.stats['checkers']['wins']} ({math.floor(u.stats['checkers']['wins'] / (u.stats['checkers']['wins'] + u.stats['checkers']['losses'])) * 100})% Winrate\n\nAchievements: {u.achievement_str('checkers')}", inline = False)
    if u.stats["chess"]["wins"] + u.stats["chess"]["losses"] > 0: embed.add_field(name = "Chess",  value = f"Skill Rating (SR): {math.floor(u.sr['chess'])}\nGames Played: {u.stats['chess']['wins'] + u.stats['chess']['losses']}\nGames Won: {u.stats['chess']['wins']} ({math.floor(u.stats['chess']['wins'] / (u.stats['chess']['wins'] + u.stats['chess']['losses'])) * 100})% Winrate\n\nAchievements: {u.achievement_str('chess')}", inline = False)
    if u.stats["gridlock"]["wins"] + u.stats["gridlock"]["losses"] > 0: embed.add_field(name = "Gridlock",  value = f"Skill Rating (SR): {math.floor(u.sr['gridlock'])}\nGames Played: {u.stats['gridlock']['wins'] + u.stats['gridlock']['losses']}\nGames Won: {u.stats['gridlock']['wins']} ({math.floor(u.stats['gridlock']['wins'] / (u.stats['gridlock']['wins'] + u.stats['gridlock']['losses'])) * 100})% Winrate\nHolo Cards Owned: {gridlock_holos}\n**Packs:** {u.packs[gridlock.Pack.SMALL]} Small, {u.packs[gridlock.Pack.LARGE]} Large, {u.packs[gridlock.Pack.PREMIUM]} Premium\n\nAchievements: {u.achievement_str('gridlock')}", inline = False)
    if u.stats["hangman"]["wins"] + u.stats["hangman"]["losses"] > 0: embed.add_field(name = "Hangman",  value = f"Games Played: {u.stats['hangman']['wins'] + u.stats['hangman']['losses']}\n\nGames Won: {u.stats['hangman']['wins']} ({math.floor(u.stats['hangman']['wins'] / (u.stats['hangman']['wins'] + u.stats['hangman']['losses'])) * 100})% Winrate\n\nAchievements: {u.achievement_str('hangman')}", inline = False)
    if u.stats["trust"]["wins"] + u.stats["trust"]["losses"] > 0: embed.add_field(name = "trust",  value = f"Games Played: {u.stats['trust']['wins'] + u.stats['trust']['losses']}\nGames Won: {u.stats['trust']['wins']} ({math.floor(u.stats['trust']['wins'] / (u.stats['trust']['wins'] + u.stats['trust']['losses'])) * 100})% Winrate\n\nVariants Owned: {variant_str}\nAchievements: {u.achievement_str('trust')}", inline = False)
    if u.stats["rps"]["wins"] + u.stats["rps"]["losses"] > 0: embed.add_field(name = "Rock Paper Scissors",  value = f"Games Played: {u.stats['rps']['wins'] + u.stats['rps']['losses']}\n\nGames Won: {u.stats['rps']['wins']} ({math.floor(u.stats['rps']['wins'] / (u.stats['rps']['wins'] + u.stats['rps']['losses'])) * 100})% Winrate\n\nAchievements: {u.achievement_str('rps')}", inline = False)
    if u.stats["slots"]["wins"] + u.stats["slots"]["losses"] > 0: embed.add_field(name = "Blackjack",  value = f"Games Played: {u.stats['slots']['wins'] + u.stats['slots']['losses']}\n\nAchievements: {u.achievement_str('slots')}", inline = False)
    if u.stats["tictactoe"]["wins"] + u.stats["tictactoe"]["losses"] > 0: embed.add_field(name = "Tic Tac Toe",  value = f"Games Played: {u.stats['tictactoe']['wins'] + u.stats['tictactoe']['losses']}\n\nGames Won: {u.stats['tictactoe']['wins']} ({math.floor(u.stats['tictactoe']['wins'] / (u.stats['tictactoe']['wins'] + u.stats['tictactoe']['losses'])) * 100})% Winrate\n\nAchievements: {u.achievement_str('tictactoe')}", inline = False)

    await ctx.interaction.followup.send(embed = embed, view = view)

# @bot.user_command(name="Challenge to a Game")
# async def profileUserCommand(ctx, user: discord.Member):
#     await ctx.defer(ephemeral = True)

# ========================================================================================================================
# /game commands
# ========================================================================================================================
@play.command(name = "bamboozle", description = "Fight to accomplish the goals of your secret role without getting lynched!")
async def bamboozlePlayCommand(ctx):
    await ctx.defer(ephemeral = False)
    if ctx.author.bot: return

    await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer, ephemeral = True))
    # await ctx.defer(ephemeral = False)
    # if ctx.author.bot: return

    # user = User(ctx.author.id)
    # if user.game() != None:
    #     g = user.game()
    #     e, v, f = g.render()
    #     g.message = await ctx.interaction.followup.send(embed = e, view = v, file = f)
    
    # else:
    #     joinButton   = discord.ui.Button(style = discord.ButtonStyle.secondary, label = "JOIN")
    #     leaveButton  = discord.ui.Button(style = discord.ButtonStyle.secondary, label = "LEAVE")
    #     startButton  = discord.ui.Button(style = discord.ButtonStyle.success,   label = "START", disabled = True)

    #     players = [ctx.author]
    #     message = None
    #     embed = discord.Embed(title = "Play BAMBOOZLE!", description = f"{ctx.author.mention} is starting a game. Press `JOIN` to join the game or `LEAVE` to leave it. Use `/info trust` to learn the basics of the game. When there are 2-8 players in the game, {ctx.author.mention} can use `START` to start the game. They can also `CANCEL` the game by deleting this message.\n\nCurrent players:\n- {ctx.author.mention}", color  = config.Color.BAMBOOZLE).set_footer(text = config.footer)
    #     view = discord.ui.View(joinButton, leaveButton, startButton, timeout = None)

    #     async def joinCallback(interaction):
    #         await interaction.response.defer(ephemeral = True)
    #         if interaction.user in players or User(interaction.user.id).game() != None:
    #             await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.IN_GAME.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
    #             return

    #         if len(players) >= 8:
    #             await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.GENERIC.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
    #             return

    #         players.append(interaction.user)
    #         User(interaction.user.id)
    #         embed.description += f"\n- {interaction.user.mention}"
    #         startButton.disabled = True if 2 <= len(players) >= 8 else False

    #         await interaction.edit_original_response(embed = embed, view = view)

    #     async def leaveCallback(interaction):
    #         await interaction.response.defer(ephemeral = True)
    #         if interaction.user.id == players[0]:
    #             await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.GENERIC.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
    #             return
            
    #         if interaction.user.id in players and User(interaction.user.id).game():
    #             players.remove(interaction.user.id)
    #             embed.description -= f"\n- {interaction.user.mention}"
    #             startButton.disabled = True if 2 <= len(players) >= 8 else False

    #             await interaction.edit_original_response(embed = embed, view = view)

    #         else:
    #             await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IN_GAME.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
    #             return

    #     async def startCallback(interaction):
    #         await interaction.response.defer(ephemeral = True)
    #         if interaction.user == players[0]:
    #             g = bamboozle.Game([bamboozle.Player(i.id, i.name) for i in players])

    #             await message.delete()
    #             e, v = g.render()
    #             g.message = await ctx.interaction.followup.send(embed = e, view = v)

    #         else:
    #             await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.PERMISSION.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
    #             return

    #     joinButton.callback   = joinCallback
    #     leaveButton.callback  = leaveCallback
    #     startButton.callback  = startCallback

    #     message = await ctx.interaction.followup.send(embed = embed, view = view)

@play.command(name = "blackjack", description = "Draw cards from the deck, trying to be closest to 21 without going over.")
async def blackjackPlayCommand(ctx, bet: discord.Option(int, "Bet an amount between 2 and 500 chips.")):
    await ctx.defer(ephemeral = True)
    if ctx.author.bot: return

    user = User(ctx.author.id)
    if user.chips < bet: await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_ENOUGH.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
    else:
        g = blackjack.Game(user, bet)
        e, v = g.render()

        g.message = await ctx.interaction.followup.send(embed = e, view = v)
    
@play.command(name = "whiteonblack", description = "Find the funniest response to the Czar\'s prompts!")
# @discord.is_nsfw()
async def whiteonblackPlayCommand(ctx, packs: discord.Option(str, "Name packs to use, separated by commas") = None):
    await ctx.defer()
    if ctx.author.bot: return

    expansions: List[whiteonblack.Expansion] = []
    user = User(ctx.author.id)

    if not packs: expansions == [whiteonblack.Expansion.BASE]
    else:
        for p in packs.lower().split(", "):
            for e in whiteonblack.Expansion:
                if not e in user.expansions: await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = f"❌ You do not own {e.value}! You can purchase it with /shop.", color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                elif p == e.value: expansions += e

    embed = discord.Embed(title = "Play White on Black!", description = f"{ctx.author.mention} is starting a game. Click `JOIN` to join the game or `LEAVE` to leave it. Use `/info whiteonblack` to learn the basics of the game. When there are 2-10 players in the game, {ctx.author.mention} can use `START` to start the game. They can also cancel the game by deleting this message.\n\nCurrent players:\n- {ctx.author.mention}", color  = config.Color.COLORLESS).set_footer(text = config.footer)
    if user.game() is not None: 
        g = user.game()
        c, e, v = g.render()
        g.message = await ctx.interaction.followup.send(content = c, embeds = e, view = v)
        user.save()
    
    else:
        view = discord.ui.View(timeout = None)
        players = [ctx.author]
        message = None

        joinButton   = discord.ui.Button(style = discord.ButtonStyle.secondary, label = "JOIN")
        leaveButton  = discord.ui.Button(style = discord.ButtonStyle.secondary, label = "LEAVE")
        startButton  = discord.ui.Button(style = discord.ButtonStyle.success,   label = "START", disabled = True)

        async def joinCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user in players or User(interaction.user.id).game(): 
                await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.IN_GAME.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                return

            if len(players) >= 10:
                await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.GENERIC.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                return

            User(interaction.user.id)
            players.append(interaction.user)
            embed.description += f"\n- {interaction.user.mention}"
            startButton.disabled = True if 3 <= len(players) >= 10 else False

            await interaction.edit_original_response(embed = embed, view = view)

        async def leaveCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user.id == players[0]:
                await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.GENERIC.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                return
            
            if interaction.user.id in players:
                players.remove(interaction.user.id)
                embed.description -= f"\n- {interaction.user.mention}"
                startButton.disabled = True if 2 <= len(players) >= 10 else False

                await interaction.edit_original_response(embed = embed, view = view)

            else:
                await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.GENERIC.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                return

        async def startCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user == players[0]:
                g = whiteonblack.Game([whiteonblack.Player(i.id, i.name) for i in players], expansions)
                c, e, v = g.render()

                await message.delete()
                g.message = await ctx.interaction.followup.send(content = c, embeds = e, view = v)

            else: await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.PERMISSION.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)

        joinButton.callback   = joinCallback
        leaveButton.callback  = leaveCallback
        startButton.callback  = startCallback

        view.add_item(joinButton)
        view.add_item(leaveButton)
        view.add_item(startButton)

        message = await ctx.interaction.followup.send(embed = embed, view = view)

@play.command(name = "checkers", description = "Capture all your opponent's pieces to claim victory!")
async def checkersPlayCommand(ctx):
    await ctx.defer(ephemeral = False)
    if ctx.author.bot: return

    await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer, ephemeral = True))

@play.command(name = "chess", description = "Battle it out in this classic game of strategy")
async def chessPlayCommand(ctx):
    await ctx.defer(ephemeral = False)
    if ctx.author.bot: return

    await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer, ephemeral = True))

@play.command(name = "gridlock", description = "Collect cards and play them on a 5x5 grid to outsmart your opponents!")
async def gridlockPlayCommand(ctx):
    await ctx.defer(ephemeral = False)
    if ctx.author.bot: return

    await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer, ephemeral = True))

@play.command(name = "hangman", description = "Try and guess a word before you get hanged!")
async def hangmanPlayCommand(ctx):
    await ctx.defer(ephemeral = True)
    if ctx.author.bot: return

    user = User(ctx.author.id)
    if user.plays["hangman"] < 1: await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_ENOUGH.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
    else:
        g = hangman.Game(user)
        e, v = g.render()
        g.message = await ctx.interaction.followup.send(embed = e, view = v)

@play.command(name = "holdem", description = "Get lucky and bluff your friends to win big!")
async def holdemPlayCommand(ctx):
    await ctx.defer(ephemeral = False)
    if ctx.author.bot: return

    await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer, ephemeral = True))

@play.command(name = "trust", description = "Race other players to buy up properties without going bankrupt!")
async def trustPlayCommand(ctx):
    await ctx.defer(ephemeral = False)
    if ctx.author.bot: return

    user = User(ctx.author.id)
    if user.game() != None:
        g = user.game()
        e, v, f = g.render()
        g.message = await ctx.interaction.followup.send(embed = e, view = v, file = f)
    
    else:
        joinButton   = discord.ui.Button(style = discord.ButtonStyle.secondary, label = "JOIN")
        leaveButton  = discord.ui.Button(style = discord.ButtonStyle.secondary, label = "LEAVE")
        startButton  = discord.ui.Button(style = discord.ButtonStyle.success,   label = "START", disabled = True)

        players = [ctx.author]
        message = None
        embed = discord.Embed(title = "Play Trust!", description = f"{ctx.author.mention} is starting a game. Press `JOIN` to join the game or `LEAVE` to leave it. Use `/info trust` to learn the basics of the game. When there are 2-8 players in the game, {ctx.author.mention} can use `START` to start the game. They can also `CANCEL` the game at any time.\n\nCurrent players:\n- {ctx.author.mention}", color  = config.Color.HELLARED).set_footer(text = config.footer)
        view = discord.ui.View(joinButton, leaveButton, startButton, timeout = None)

        async def joinCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user in players or User(interaction.user.id).game() != None:
                await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.IN_GAME.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                return

            if len(players) >= 8:
                await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.GENERIC.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                return

            players.append(interaction.user)
            User(interaction.user.id)
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

        async def startCallback(interaction):
            await interaction.response.defer(ephemeral = True)
            if interaction.user == players[0]:
                g = trust.Game([trust.Player(i.id, i.name) for i in players])

                await message.delete()
                e, v, f = g.render()
                g.message = await ctx.interaction.followup.send(embed = e, view = v, file = f)

            else:
                await interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.PERMISSION.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
                return

        joinButton.callback   = joinCallback
        leaveButton.callback  = leaveCallback
        startButton.callback  = startCallback

        message = await ctx.interaction.followup.send(embed = embed, view = view)

@play.command(name = "quickdraw", description = "Whoever draws first after the countdown wins!")
async def quickdrawPlayCommand(ctx, user: discord.Option(discord.Member, "Challenge this user to a quickdraw game!")):
    await ctx.defer(ephemeral = False)
    if ctx.author.bot: return

    await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer, ephemeral = True))
    # await ctx.defer(ephemeral = False)
    # if ctx.author.bot: return

    # acceptButton = discord.ui.Button(label = "ACCEPT CHALLENGE", style = discord.ButtonStyle.secondary)
    # message: discord.Message = None

    # async def acceptCallback(interaction):
    #     await interaction.response.defer(ephemeral = False)
    #     if interaction.user.id != user.id: await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.PERMISSION.value, color = config.Color.ERROR).set_footer(text = config.footer, ephemeral = True))
    #     else:
    #         await message.edit(embed = discord.Embed(title = f"{user.name} has accepted {ctx.author.name}'s challenge to a Quickdraw!", description = "A countdown has been started. After the countdown, a 💥 will appear, and the first player to click it wins!", color = config.Color.COLORLESS).set_footer(text = config.footer), view = discord.ui.View())
    #         await asyncio.sleep(random.randint(2, 15))
    #         await message.add_reaction("💥")

    #         try: _, u, = await bot.wait_for("reaction_add", check = lambda r, u: u in [ctx.author, user] and str(r.emoji) == "💥", timeout = 30)
    #         except asyncio.TimeoutError: await message.edit(embed = discord.Embed(title = f"☁️ Huh? No one drew in time.", color = config.Color.COLORLESS).set_footer(text = config.footer))
    #         else: 
    #             await message.edit(embed = discord.Embed(title = f"💥 Bang! {u.name} draws first!", color = config.Color.COLORLESS).set_footer(text = config.footer))
    #             await message.clear_reactions()

    # acceptButton.callback = acceptCallback
    # message = await ctx.interaction.followup.send(embed = discord.Embed(title = f"{ctx.author.name} has challenged {user.name} to a Quickdraw!", description = "When they accept the challenge, a countdown will start. After the countdown, a 💥 will appear, and the first player to click it wins!", color = config.Color.COLORLESS).set_footer(text = config.footer), view = discord.ui.View(acceptButton), ephemeral = True)

@play.command(name = "rockpaperscissors", description = "Rock beats scissors, paper beats rock, and scissors beat paper.")
async def rockpaperscissorsPlayCommand(ctx):
    await ctx.defer(ephemeral = False)
    if ctx.author.bot: return

    await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer, ephemeral = True))

@play.command(name = "slots", description = "Get 3 in a row to win big!")
async def slotsPlayCommand(ctx):
    await ctx.defer(ephemeral = False)
    if ctx.author.bot: return

    await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer, ephemeral = True))

@play.command(name = "tictactoe", description = "Get 3 in a row before your opponent can.")
async def tictactoePlayCommand(ctx):
    await ctx.defer(ephemeral = False)
    if ctx.author.bot: return

    await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_IMPLEMENTED.value, color = config.Color.ERROR).set_footer(text = config.footer, ephemeral = True))

@play.command(name = "twentyfortyeight", description = "Merge tiles until you run out of space.")
async def twentyfortyeightPlayCommand(ctx):
    await ctx.defer(ephemeral = True)
    if ctx.author.bot: return

    user = User(ctx.author.id)
    if user.plays["2048"] < 1: await ctx.interaction.followup.send(embed = discord.Embed(title = random.choice(config.error_titles), description = config.Error.NOT_ENOUGH.value, color = config.Color.ERROR).set_footer(text = config.footer), ephemeral = True)
    else:
        g = twentyfortyeight.Game(user)
        e, v, f = g.render()
        g.message = await ctx.interaction.followup.send(embed = e, view = v, file = f)

if __name__ == "__main__":
    bot.run(config.token)
    input()