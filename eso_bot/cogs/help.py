import discord
from eso_bot.backend import functions
from discord.ext import commands
import sqlite3

conn = sqlite3.connect("prefix.db", timeout=5.0)
c = conn.cursor()
conn.row_factory = sqlite3.Row


class Help(commands.Cog, name="Help"):
    def __init__(self, bot):
        self.bot = bot
        print("help.py extension has loaded!")

    commands.command(
        name="help",
        description="The help command!",
        aliases=["commands", "command"],
        usage="cog",
    )

    @commands.command()
    async def help(self, ctx):
        await functions.dailyCommandCounter("help")
        await functions.globalCommandCounter("help")
        await functions.commandCounter(ctx.author.id, "help")
        reactions = ["🌴", "🛠️", "❓"]
        reactionsCogs = ["🌴 Lookup", "🛠️ Settings", "❓ Information"]
        cogs = [cog for cog in self.bot.cogs.keys()]
        prefixDictionary = {}
        for prefix in c.execute("SELECT guild_id, prefix FROM prefix"):
            prefixDictionary.update({prefix[0]: f"{prefix[1]}"})
        currentPrefix = prefixDictionary[ctx.message.guild.id]
        embed = discord.Embed(
            title="Bot Help Menu",
            description=f"`{currentPrefix}myprefix` for this server's prefix and `{currentPrefix}setprefix` "
            f"to change this server's prefix.",
            colour=functions.embedColour(ctx.guild.id),
        )
        # embed.set_thumbnail(url="https://i.imgur.com/3Lgs39V.png")
        embed.set_footer(
            text=f"Requested by {ctx.message.author.name} :: {ctx.message.guild}'s prefix currently is {currentPrefix}",
            icon_url=self.bot.user.avatar_url,
        )
        hidden_cogs = ["Help", "Functions"]
        for cog in cogs:
            if cog not in hidden_cogs:
                try:
                    cog_commands = self.bot.get_cog(cog).get_commands()
                    commands_list = ""
                    for comm in cog_commands:
                        commands_list += f"`{comm}` "
                    embed.add_field(name=cog, value=commands_list, inline=True)
                except Exception as e:
                    print(str(e))
        msg = await ctx.send(embed=embed)
        for react in reactions:
            await msg.add_reaction(react)

        def check(reaction, user):
            return (
                str(reaction.emoji) in reactions
                and user == ctx.message.author
                and reaction.message.id == msg.id
            )

        async def handle_reaction(reaction, msg, check):
            await msg.remove_reaction(reaction, ctx.message.author)
            reactionIndex = reactions.index(str(reaction.emoji))
            if str(reaction.emoji) == reactions[reactionIndex]:
                help_embed = discord.Embed(
                    title=f"{reactionsCogs[reactionIndex]} Help",
                    colour=functions.embedColour(ctx.guild.id),
                )
                help_embed.set_footer(
                    text=f"Requested by {ctx.message.author.name} :: {ctx.message.guild}'s prefix currently "
                    f"is {currentPrefix}",
                    icon_url=self.bot.user.avatar_url,
                )
                cog_commands = self.bot.get_cog(
                    f"{reactionsCogs[reactionIndex]}"
                ).get_commands()
                commands_list = ""
                for comm in cog_commands:
                    commands_list += f"**{comm.name}** - {comm.description}\n"
                    help_embed.add_field(name=comm, value=comm.description, inline=True)
                await msg.edit(embed=help_embed)
            else:
                return
            reaction, user = await self.bot.wait_for(
                "reaction_add", check=check, timeout=30
            )
            await handle_reaction(reaction, msg, check)

        reaction, user = await self.bot.wait_for(
            "reaction_add", check=check, timeout=30
        )
        await handle_reaction(reaction, msg, check)


def setup(bot):
    bot.add_cog(Help(bot))
