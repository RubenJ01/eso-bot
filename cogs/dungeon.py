import json
import discord
import datetime
import asyncio

import pytz
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
        result = False
        dungeon = " ".join(dungeon)
        pages = []
        timezone = pytz.timezone("Europe/Amsterdam")
        time = timezone.localize(datetime.datetime.now())
        for x in data:
            if x["dungeon"].lower() == dungeon.lower():
                result = True
                embed = discord.Embed(title=x["dungeon"], description=x["description"], url=x["link"], timestamp=time)
                embed.add_field(name="Sets", value=", ".join([x for x in x["sets"]]), inline=False)
                bosses = ""
                for boss in x["bosses"]:
                    bosses += f"`{boss['name']}`\n"
                embed.add_field(name="Bosses", value=bosses)
                pages.append(embed)
                for boss in x["bosses"]:
                    embed = discord.Embed(title=boss['name'], timestamp=time)
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
        if result is not True:
            if not dungeon:
                dungeon = "none"
            results = ""
            loaded_dungeons = [x["dungeon"] for x in data]
            for index, x in enumerate(loaded_dungeons):
                results += f"`{index + 1}` {x} \n"
            embed = discord.Embed(title="Dungeons",
                                  description=f"`{dungeon}` was not found.\nPlease choose one of the following "
                                              f"dungeons:\n{results}\nReply "
                                              f"with a number for more information.",
                                  timestamp=time)
            await ctx.send(embed=embed)

            def check(m):
                return m.content in [str(i) for i in range(1, len(loaded_dungeons) + 1)] \
                       and m.channel == ctx.channel and ctx.author == m.author

            try:
                choice = await ctx.bot.wait_for('message', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                return await ctx.send("Request timed out.")
            if choice:
                dungeon = f'{loaded_dungeons[int(choice.content) - 1].lower()}'
                await ctx.send(f'!dungeon {dungeon}')
                async with ctx.typing():
                    return await ctx.invoke(self.dungeon_command, dungeon)


def setup(bot):
    bot.add_cog(Lookup(bot))
