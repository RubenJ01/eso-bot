import discord
import datetime
import pytz
import math
import sqlite3
import traceback
from discord.ext import commands, tasks
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
        self.loggingChecker.start()

    @tasks.loop(seconds=5)
    async def loggingChecker(self):
        timezone_ = pytz.timezone("Europe/Amsterdam")
        lastMidnight = (
            datetime.datetime.now(timezone_)
            .replace(hour=0, minute=0, second=0, microsecond=0)
            .timestamp()
        )
        now = int(datetime.datetime.now(timezone_).timestamp())
        c.execute(""" SELECT command, times, nextReset FROM dailyLogging """)
        result = c.fetchall()
        if not result:
            pass
        else:
            if lastMidnight + 5 > now > lastMidnight:
                descriptionList = ""
                for commandProperties in result:
                    nextReset = commandProperties[2]
                    if now > nextReset:
                        descriptionList += f"`{commandProperties[0]}`. Used {commandProperties[1]} times.\n"
                        c.execute(
                            """ DELETE FROM dailyLogging WHERE command = ? """,
                            (commandProperties[0],),
                        )
                        conn.commit()
                yesterday = datetime.datetime.now(timezone_) - datetime.timedelta(1)
                embed = discord.Embed(
                    title=f"{yesterday.date()}",
                    description=f"{descriptionList}",
                    timestamp=datetime.datetime.now(timezone_),
                )

                def sortSecond(val):
                    return val[1]

                result.sort(key=sortSecond, reverse=True)
                embed.add_field(
                    name="Most Used Command", value=f"{result[0][0]}", inline=False
                )
                channelObject = self.bot.get_channel(logsChannel)
                await channelObject.send(embed=embed)

    @loggingChecker.before_loop
    async def before_status(self):
        print("Waiting to handle loggings...")
        await self.bot.wait_until_ready()

    @commands.command(description="`!profile`\n\nShows profile of the user!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def profile(self, ctx, user: discord.Member = None):
        if user:
            id = user.id
        else:
            id = ctx.author.id

        descriptionList = ""
        c.execute(""" SELECT command, times FROM logging WHERE user_id = ? """, (id,))
        result = c.fetchall()

        for command in result:
            descriptionList += f"`{command[0]}`: used {command[1]} times\n"

        c.execute(
            """ SELECT command FROM mostRecent WHERE user_id = ? """, (ctx.author.id,)
        )
        mostRecentCommand = c.fetchall()

        if user:
            embed = discord.Embed(
                description=f"{descriptionList}",
                colour=functions.embedColour(ctx.message.guild.id),
            )
        else:
            embed = discord.Embed(
                description=f"{descriptionList}",
                colour=functions.embedColour(ctx.message.guild.id),
            )

        if not result:
            embed.add_field(name="Most Used Command", value="None", inline=False)
        else:

            def sortSecond(val):
                return val[1]

            result.sort(key=sortSecond, reverse=True)
            embed.add_field(
                name="Most Used Command", value=f"{result[0][0]}", inline=False
            )

        if mostRecentCommand:
            commandUsed = mostRecentCommand[0][0]
            embed.add_field(
                name="Most Recent Command", value=f"{commandUsed}", inline=False
            )
        else:
            embed.add_field(name="Most Recent Command", value="None", inline=False)

        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(description="`!invite`\n\nSends the invite link for the bot!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx):
        await ctx.send(
            "https://discord.com/oauth2/authorize?client_id=572365749780348928&permissions=0&scope=bot"
        )
        await functions.dailyCommandCounter("invite")
        await functions.globalCommandCounter("invite")
        await functions.commandCounter(ctx.author.id, "invite")

    @commands.command(
        description="`!counter`\n\nShows the global counter for commands used. Administrator Only."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def counter(self, ctx):
        descriptionList = ""
        c.execute(""" SELECT command, times FROM globalLogging """)
        result = c.fetchall()

        for command in result:
            descriptionList += f"`{command[0]}`: used {command[1]} times\n"

        embed = discord.Embed(
            description=f"{descriptionList}",
            colour=functions.embedColour(ctx.message.guild.id),
        )

        if not result:
            embed.add_field(name="Most Used Command", value="None", inline=False)
        else:

            def sortSecond(val):
                return val[1]

            result.sort(key=sortSecond, reverse=True)
            embed.add_field(
                name="Most Used Command", value=f"{result[0][0]}", inline=False
            )

        embed.set_author(name=ctx.guild, icon_url=ctx.guild.icon_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(
        description="`!embedsettings {colour code e.g. 0xffff0}`\n\n Changes the color of the embeds "
        "for a guild."
    )
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

    @commands.command(description="`!status` \n\nSends the bots status.")
    async def status(self, ctx):
        await functions.dailyCommandCounter("status")
        await functions.globalCommandCounter("status")
        await functions.commandCounter(ctx.author.id, "status")
        status_embed = discord.Embed(
            title="Status", colour=functions.embedColour(ctx.guild.id)
        )
        members = len(list(self.bot.get_all_members()))
        uptime = datetime.datetime.now() - self.bot.start_time
        uptime = datetime.timedelta(days=uptime.days, seconds=uptime.seconds)
        date = "**Created on:** 30-9-2018"
        status_embed.description = "\n".join(
            [
                f"Bot up and running in {len(self.bot.guilds)} guilds with {members} members.",
                f"**Uptime:** {uptime}\n{date}",
                "For more help or information join our [support server](https://discord.gg/5xvAHhU)",
            ]
        )
        status_embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        status_embed.set_footer(text="Use !help to get a list of available commands.")
        return await ctx.send(embed=status_embed)

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
