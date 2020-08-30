import json
import discord

from discord.ext.commands import Cog, command
from discord.ext import buttons


class Paginator(buttons.Paginator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Lookup(Cog, name='Lookup commands'):
    def __init__(self, bot):
        self.bot = bot

    @command(name="dungeon")
    async def dungeon_command(self, ctx, *dungeon):
        with open('assets/dungeons.json', 'r') as dungeons:
            data = json.load(dungeons)
        dungeon = " ".join(dungeon)
        for x in data:
            if x["dungeon"].lower() == dungeon.lower():
                embed = discord.Embed(title=x["dungeon"], description=x["description"])
                description = ""
                for boss in x["bosses"]:
                    description += f"{boss['name']}\n**Mechanics**\n"
                    for mechanic in boss["mechanics"]:
                        description += f"-{mechanic}\n"
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Lookup(bot))

