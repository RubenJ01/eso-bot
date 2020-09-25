import json
import discord

from backend import functions

from discord.ext.commands import Cog, command


class Information(Cog, name="❓ Information"):
    def __init__(self, bot):
        self.bot = bot

    @command(description="`!dailies`\n\nAll of the daily rewards this month.")
    async def dailies(self, ctx):
        with open("assets/dailies.json", "r", encoding="utf-8") as dailies:
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


def setup(bot):
    bot.add_cog(Information(bot))
