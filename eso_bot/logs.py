import discord
import datetime
import pytz
import math
import sqlite3
import traceback
from discord.ext import commands
from discord.ext.commands import has_permissions

from eso_bot.backend import functions
from eso_bot.authentication import logsChannel


conn = sqlite3.connect("bot.db", timeout=5.0)
c = conn.cursor()
conn.row_factory = sqlite3.Row

timezone = pytz.timezone("Europe/Amsterdam")
time = timezone.localize(datetime.datetime.now())


class Logs(commands.Cog, name="🛠️ Settings"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="`!invite`\n\nSends the invite link for the bot!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx):

        await ctx.send(
            "https://discord.com/oauth2/authorize?client_id=572365749780348928&permissions=0&scope=bot"
        )

    @commands.command(description="`/embedsettings [colour code e.g. 0xffff0]`\n\n")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @has_permissions(administrator=True)
    async def embedsettings(self, ctx, colour):

        try:
            c.execute(
                """ UPDATE SERVER SET embed = ? WHERE server_id = ? """,
                (colour, ctx.message.guild.id),
            )
            conn.commit()
            await functions.requestEmbedTemplate(
                ctx,
                f"☑️ Embed colour successfully set to `{colour}` for `{ctx.message.guild}`.",
                ctx.message.author,
            )
        except ValueError:

            traceback.print_exc()

    @commands.Cog.listener()
    async def on_ready(self):

        embed = discord.Embed(
            title="on_ready()", description="Bot succesfully started.", timestamp=time
        )
        channel = self.bot.get_channel(logsChannel)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):

            seconds = error.retry_after
            minutes = seconds / 60
            hours = seconds / 3600

            if seconds / 60 < 1:

                embed = discord.Embed(
                    description=f"You're using this command too often! Try again in {str(int(seconds))} seconds!"
                )
                await ctx.send(embed=embed)

            elif minutes / 60 < 1:

                embed = discord.Embed(
                    description=f"You're using this command too often! Try again in {math.floor(minutes)} minutes and "
                    f"{(int(seconds) - math.floor(minutes) * 60)} seconds!"
                )
                await ctx.send(embed=embed)

            else:

                embed = discord.Embed(
                    description=f"You're using this command too often! Try again in {math.floor(hours)} hours, "
                    f"{(int(minutes) - math.floor(hours) * 60)} minutes, "
                    f"{(int(seconds) - math.floor(minutes) * 60)} seconds!"
                )
                await ctx.send(embed=embed)

        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                description="You do not have the permission to do this!"
            )
            await ctx.send(embed=embed)

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description="Missing arguments on your command! Please check and retry again!"
            )
            await ctx.send(embed=embed)
        embed = discord.Embed(title="Error", description=f"{error}", timestamp=time)
        channel = self.bot.get_channel(logsChannel)
        await channel.send(embed=embed)
        raise error


def setup(bot):
    bot.add_cog(Logs(bot))
