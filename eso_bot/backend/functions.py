import discord
from discord.ext import commands
import sqlite3
import pytz
import datetime

conn = sqlite3.connect("bot.db", timeout=5.0)
c = conn.cursor()
conn.row_factory = sqlite3.Row

c.execute(
    """CREATE TABLE IF NOT EXISTS server (`server_id` INT PRIMARY KEY, `embed` STR) """
)
c.execute(
    """ CREATE TABLE IF NOT EXISTS logging (`user_id` INT, `command` STR, `times` INT, UNIQUE(user_id, command))"""
)
c.execute(
    """ CREATE TABLE IF NOT EXISTS mostRecent (`user_id` INT PRIMARY KEY, `command` STR) """
)
c.execute(
    """ CREATE TABLE IF NOT EXISTS globalLogging (`command` STR PRIMARY KEY, `times` INT) """
)
c.execute(
    """ CREATE TABLE IF NOT EXISTS dailyLogging (`command` STR PRIMARY KEY, `times` INT, `nextReset` INT) """
)


async def dailyCommandCounter(commandType):
    timezone = pytz.timezone("Europe/Amsterdam")
    lastMidnight = (
        datetime.datetime.now(timezone)
        .replace(hour=0, minute=0, second=0, microsecond=0)
        .timestamp()
    )
    nextMidnight = int(lastMidnight) + 86400
    c.execute(""" SELECT times FROM dailyLogging WHERE command = ? """, (commandType,))
    databaseCheck = c.fetchall()
    if not databaseCheck:
        c.execute(
            """ INSERT OR REPLACE INTO dailyLogging VALUES (?, ?, ?) """,
            (commandType, 1, nextMidnight),
        )
        conn.commit()
    else:
        counter = int(databaseCheck[0][0])
        counter += 1
        c.execute(
            """ INSERT OR REPLACE INTO dailyLogging VALUES (?, ?, ?) """,
            (commandType, counter, nextMidnight),
        )
        conn.commit()


async def globalCommandCounter(commandType):
    c.execute(""" SELECT times FROM globalLogging WHERE command = ? """, (commandType,))
    databaseCheck = c.fetchall()
    if not databaseCheck:
        c.execute(
            """ INSERT OR REPLACE INTO globalLogging VALUES (?, ?) """, (commandType, 1)
        )
        conn.commit()
    else:
        counter = int(databaseCheck[0][0])
        counter += 1
        c.execute(
            """ INSERT OR REPLACE INTO globalLogging VALUES (?, ?) """,
            (commandType, counter),
        )
        conn.commit()


async def commandCounter(user, commandType):
    c.execute(
        """ SELECT command, times FROM logging WHERE user_id = ? AND command = ? """,
        (user, commandType),
    )
    databaseCheck = c.fetchall()
    if not databaseCheck:
        c.execute(
            """ INSERT OR REPLACE INTO logging VALUES (?, ?, ?) """,
            (user, commandType, 1),
        )
        conn.commit()
    else:
        counter = int(databaseCheck[0][1])
        counter += 1
        c.execute(
            """ UPDATE logging SET times = ? WHERE user_id = ? AND command = ? """,
            (counter, user, commandType),
        )
        conn.commit()

    c.execute(
        """ INSERT OR REPLACE INTO mostRecent VALUES (?, ?) """, (user, commandType)
    )
    conn.commit()


async def requestEmbedTemplate(ctx, description, author):
    embed = discord.Embed(
        description=f"{description}", colour=embedColour(ctx.message.guild.id)
    )
    embed.set_footer(text=f"Requested by {author}", icon_url=author.avatar_url)
    return await ctx.send(embed=embed)


def embedColour(guild):
    for row in c.execute(f"SELECT embed FROM server WHERE server_id = {guild}"):
        colourEmbed = row[0]
        colourEmbedInt = int(colourEmbed, 16)
        return colourEmbedInt


def createGuildProfile(ID):
    c.execute(""" INSERT OR REPLACE INTO server VALUES (?, ?) """, (ID, "0xffff00"))
    conn.commit()
    print(f"Added for {ID} into guild database.")


class Functions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        guild_database = []

        for row in c.execute("SELECT server_id FROM server"):
            guild_database.append(row[0])

        if guild.id not in guild_database:
            createGuildProfile(guild.id)

    @commands.Cog.listener()
    async def on_ready(self):

        guild_database = []

        for guild in c.execute("SELECT server_id FROM server"):
            guild_database.append(guild[0])

        for guild in self.bot.guilds:

            if guild.id not in guild_database:
                createGuildProfile(guild.id)


def setup(bot):
    bot.add_cog(Functions(bot))
