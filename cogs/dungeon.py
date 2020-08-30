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
        pages = []
        for x in data:
            if x["dungeon"].lower() == dungeon.lower():
                embed = discord.Embed(title=x["dungeon"], description=x["description"], url=x["link"])
                embed.add_field(name="Sets", value=", ".join([x for x in x["sets"]]), inline=False)
                bosses = ""
                for boss in x["bosses"]:
                    bosses += f"`{boss['name']}`\n"
                embed.add_field(name="Bosses", value=bosses)
                pages.append(embed)
                for boss in x["bosses"]:
                    embed = discord.Embed(title=boss['name'])
                    mechanics = ""
                    for mechanic in boss["mechanics"]:
                        mechanics += f"-{mechanic}\n"
                    embed.add_field(name="Mechanics", value=mechanics)
                    strategies = ""
                    for strategy in boss["strategy"]:
                        strategies += f"-{strategy}\n"
                    embed.add_field(name="Strategies", value=strategies)
                    pages.append(embed)
                final_embed = Paginator(embed=False, timeout=90, use_defaults=True,
                                        extra_pages=pages, length=1)
                await final_embed.start(ctx)
        return await ctx.send(f"`{dungeon}` was not found.")


def setup(bot):
    bot.add_cog(Lookup(bot))
