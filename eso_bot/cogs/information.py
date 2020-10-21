import json
import discord
import datetime
import pytz

from eso_bot.backend import functions

from discord.ext.commands import Cog, command


class Information(Cog, name="❓ Information"):
    def __init__(self, bot):
        self.bot = bot

    @command(description="`!dailies`\n\nAll of the daily rewards this month.")
    async def dailies(self, ctx):
        await functions.dailyCommandCounter("dailies")
        await functions.globalCommandCounter("dailies")
        await functions.commandCounter(ctx.author.id, "dailies")
        with open("eso_bot/assets/dailies.json", "r", encoding="utf-8") as dailies:
            data = json.load(dailies)[0]
        daily_rewards_1 = discord.Embed(
            title="Daily Rewards (Day 1-15)", colour=functions.embedColour(ctx.guild.id)
        )
        for day in data["rewards"][:15]:
            daily_rewards_1.add_field(
                name=f"Day {day['day']}",
                value=f"{day['reward']} {self.bot.get_emoji(day['emoji'])}",
            )
        daily_rewards_1.set_footer(text=data["date"])
        daily_rewards_2 = discord.Embed(
            title="Daily Rewards (Day 15-30)",
            colour=functions.embedColour(ctx.guild.id),
        )
        for day in data["rewards"][15:]:
            daily_rewards_2.add_field(
                name=f"Day {day['day']}",
                value=f"{day['reward']} {self.bot.get_emoji(day['emoji'])}",
            )
        daily_rewards_2.set_footer(text=data["date"])
        await ctx.send(embed=daily_rewards_1)
        return await ctx.send(embed=daily_rewards_2)

    @command(
        description="`!links`\n\nSeveral helpfull links with valueable information."
    )
    async def links(self, ctx):
        await functions.dailyCommandCounter("links")
        await functions.globalCommandCounter("links")
        await functions.commandCounter(ctx.author.id, "links")
        timezone = pytz.timezone("Europe/Amsterdam")
        time = timezone.localize(datetime.datetime.now())
        embed = discord.Embed(
            title="Links",
            description="https://eso-hub.com/\nhttps://elderscrollsonline.wiki.fextralife.com/Elder+Scrolls+Online+Wiki"
            + "\nhttps://alcasthq.com/",
            timestamp=time,
            colour=functions.embedColour(ctx.guild.id),
        )
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
