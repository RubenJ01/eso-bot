import discord
from discord.ext import commands
import sqlite3

conn = sqlite3.connect('bot.db', timeout=5.0)
c = conn.cursor()
conn.row_factory = sqlite3.Row

c.execute('''CREATE TABLE IF NOT EXISTS server (`server_id` INT PRIMARY KEY, `embed` STR) ''')


async def requestEmbedTemplate(ctx, description, author):
    embed = discord.Embed(description=f"{description}", colour=embedColour(ctx.message.guild.id))
    embed.set_footer(text=f"Requested by {author}", icon_url=author.avatar_url)
    return await ctx.send(embed=embed)


def embedColour(guild):
    for row in c.execute(f'SELECT embed FROM server WHERE server_id = {guild}'):
        colourEmbed = row[0]
        colourEmbedInt = int(colourEmbed, 16)
        return colourEmbedInt


def createGuildProfile(ID):
    c.execute(''' INSERT OR REPLACE INTO server VALUES (?, ?) ''', (ID, "0xffff00"))
    conn.commit()
    print(f"Added for {ID} into guild database.")


class Functions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        guild_database = []

        for row in c.execute('SELECT server_id FROM server'):
            guild_database.append(row[0])

        if guild.id not in guild_database:
            createGuildProfile(guild.id)

    @commands.Cog.listener()
    async def on_ready(self):

        guild_database = []

        for guild in c.execute('SELECT server_id FROM server'):
            guild_database.append(guild[0])

        for guild in self.bot.guilds:

            if guild.id not in guild_database:
                createGuildProfile(guild.id)


def setup(bot):
    bot.add_cog(Functions(bot))
