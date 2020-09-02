import json
import discord
import datetime
import asyncio

from backend.helpers import command_invoked

import pytz
from discord.ext.commands import Cog, command
from discord.ext import buttons


class Paginator(buttons.Paginator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Lookup(Cog, name='Lookup commands'):
    """
    Lookup information on our eso database.
    """

    def __init__(self, bot):
        self.bot = bot

    @command(name="dungeon")
    async def dungeon_command(self, ctx, *dungeon):
        """
        Request information on a specific dungeon.
        """
        user = ctx.author.name
        await command_invoked(self.bot, "dungeon", user)
        with open('eso-bot/assets/dungeons.json', 'r', encoding='utf-8') as dungeons:
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
                    strategies = ""
                    for strategy in boss["strategy"]:
                        strategies += f"-{strategy}\n"
                    mechanics = ""
                    for mechanic in boss["mechanics"]:
                        mechanics += f"-{mechanic}\n"
                    if len(mechanics) < 1024 and len(strategies) < 1024:
                        print("hello")
                        embed = discord.Embed(title=boss['name'], timestamp=time)
                        embed.add_field(name="Mechanics", value=mechanics)
                        embed.add_field(name="Strategies", value=strategies)
                        pages.append(embed)
                    else:
                        embed = discord.Embed(title=f"{boss['name']} mechanics",
                                              description=mechanics, timestamp=time)
                        pages.append(embed)
                        embed = discord.Embed(title=f"{boss['name']} strategies",
                                              description=strategies, timestamp=time)
                        pages.append(embed)
                final_embed = Paginator(embed=False, timeout=90, use_defaults=True,
                                        extra_pages=pages, length=1)
                await final_embed.start(ctx)
        if result is not True:
            if not dungeon:
                dungeon = "none"
            results = ""
            reference_dungeons = []
            for x in data:
                if dungeon != "none":
                    if dungeon.lower() in x["dungeon"].lower():
                        reference_dungeons.append(x["dungeon"])
            if len(reference_dungeons) == 1:
                return await ctx.invoke(self.dungeon_command, reference_dungeons[0])
            elif len(reference_dungeons) > 0:
                loaded_dungeons = reference_dungeons
            else:
                loaded_dungeons = [x["dungeon"] for x in data]
            for index, x in enumerate(loaded_dungeons):
                results += f"`{index + 1}` {x} \n"
            embed = discord.Embed(title="Dungeons",
                                  description=f"`{dungeon}` was not found.\nDid you mean one of the following "
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

    @command(name="set")
    async def set_command(self, ctx, *set):
        """
        Lookup information on any set.
        """
        await command_invoked(self.bot, "set", ctx.author.name)
        with open('eso-bot/assets/sets.json', 'r', encoding='utf-8') as dungeons:
            data = json.load(dungeons)
        result = False
        set_ = " ".join(set)
        if len(set_) < 3:
            return await ctx.send("Your search request must be at least 3 characters.")
        for x in data:
            if set_.lower() == x["name"].lower():
                result = True
                description = ""
                for index, effect in enumerate(x["effects"]):
                    description += f"**{index + 2} items:** {effect}\n"
                embed = discord.Embed(title=x["name"], description=description, url=x["link"])
                embed.set_thumbnail(url=x["image"])
                embed.set_footer(text="Sets and icons © by ZeniMax Online Studios")
                return await ctx.send(embed=embed)
        if result is False:
            reference_sets = []
            results = ""
            timezone = pytz.timezone("Europe/Amsterdam")
            time = timezone.localize(datetime.datetime.now())
            for x in data:
                if set_.lower() in x["name"].lower():
                    reference_sets.append(x["name"])
            if len(reference_sets) == 1:
                return await ctx.invoke(self.set_command, reference_sets[0])
            elif len(reference_sets) > 0:
                loaded_sets = reference_sets
            elif len(reference_sets) == 0:
                return await ctx.send(f"No results were found matching your request: `{set_}`")
            else:
                loaded_sets = [x["name"] for x in data]
            for index, x in enumerate(loaded_sets):
                results += f"`{index + 1}` {x} \n"
            embed = discord.Embed(title="Sets",
                                  description=f"`{set_}` was not found.\nDid you mean one of the following "
                                              f"dungeons:\n{results}\nReply "
                                              f"with a number for more information.",
                                  timestamp=time)
            await ctx.send(embed=embed)

            def check(m):
                return m.content in [str(i) for i in range(1, len(loaded_sets) + 1)] \
                       and m.channel == ctx.channel and ctx.author == m.author

            try:
                choice = await ctx.bot.wait_for('message', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                return await ctx.send("Request timed out.")
            if choice:
                set = f'{loaded_sets[int(choice.content) - 1].lower()}'
                await ctx.send(f'!set {set}')
                async with ctx.typing():
                    return await ctx.invoke(self.set_command, set)


def setup(bot):
    bot.add_cog(Lookup(bot))
