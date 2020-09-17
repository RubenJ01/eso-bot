import json
import discord
import datetime
import asyncio
import math

from eso_bot.backend import functions
from eso_bot.backend.helpers import command_invoked

import pytz
from discord.ext.commands import Cog, command
from discord.ext import buttons


class Paginator(buttons.Paginator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Lookup(Cog, name="🌴 Lookup"):
    def __init__(self, bot):
        self.bot = bot

    @command(description="`!dungeon {dungeon}`\n\nShows the dungeon list and boss' strategies!")
    async def dungeon(self, ctx, *, dungeon=None):
        with open('assets/dungeons.json', 'r', encoding='utf-8') as dungeons:
            data = json.load(dungeons)
        if not dungeon:
            reacts = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫']
            dungeonsList = ""
            pages = math.ceil(len(data) / 6)
            i = 0
            k = 1
            everyPage = [item['dungeon'] for item in data[6 * (k - 1):k * 6]]
            for item in everyPage:
                dungeonsList += f"`{reacts[i]}` {item}\n"
                i += 1
            embed = discord.Embed(title="Dungeons List",
                                  description=f"Please select from one of the following dungeons:\n{dungeonsList}",
                                  colour=functions.embedColour(ctx.guild.id))
            embed.set_footer(text=f'Requested by {ctx.message.author}',
                             icon_url=ctx.author.avatar_url)
            msg = await ctx.send(embed=embed)
            await msg.add_reaction('⏪')
            for number in reacts:
                await msg.add_reaction(number)
            await msg.add_reaction('⏩')
            def check(reaction, user):
                reactCheck = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '📖', '⏪', '⏩']
                return str(
                    reaction.emoji) in reactCheck and user == ctx.message.author and reaction.message.id == msg.id
            async def handle_rotate(reaction, msg, check, k):
                global reactionIndex
                await msg.remove_reaction(reaction, ctx.message.author)
                try:
                    reactionIndex = reacts.index(str(reaction.emoji))
                except:
                    pass
                if str(reaction.emoji) == '⏪':
                    k -= 1
                    if k <= 0:
                        embed = discord.Embed(description=f"You have reached the end of the pages!",
                                              colour=functions.embedColour(ctx.message.guild.id))
                        embed.set_thumbnail(url=f"{ctx.message.guild.icon_url}")
                        embed.set_footer(text=f"Press '⏪' to go back.", icon_url=ctx.author.avatar_url)
                        await msg.edit(embed=embed)
                    else:
                        everyPage = [item['dungeon'] for item in data[6 * (k - 1):k * 6]]
                        dungeonsList = ""
                        i = 0
                        for item in everyPage:
                            dungeonsList += f"`{reacts[i]}` {item}\n"
                            i += 1
                        embed = discord.Embed(title="Dungeons List",
                                              description=f"Please select from one of the following dungeons:\n{dungeonsList}",
                                              colour=functions.embedColour(ctx.guild.id))
                        embed.set_footer(text=f'Requested by {ctx.message.author}',
                                         icon_url=ctx.author.avatar_url)
                        await msg.edit(embed=embed)
                elif str(reaction.emoji) == '⏩':
                    k += 1
                    if k > pages:
                        embed = discord.Embed(description=f"You have reached the end of the pages!",
                                              colour=functions.embedColour(ctx.message.guild.id))
                        embed.set_thumbnail(url=f"{ctx.message.guild.icon_url}")
                        embed.set_footer(text=f"Press '⏩' to go back.", icon_url=ctx.author.avatar_url)
                        await msg.edit(embed=embed)

                    else:
                        everyPage = [item['dungeon'] for item in data[6 * (k - 1):k * 6]]
                        dungeonsList = ""
                        i = 0
                        for item in everyPage:
                            dungeonsList += f"`{reacts[i]}` {item}\n"
                            i += 1
                        embed = discord.Embed(title="Dungeons List",
                                              description=f"Please select from one of the following dungeons:\n{dungeonsList}",
                                              colour=functions.embedColour(ctx.guild.id))
                        embed.set_footer(text=f'Requested by {ctx.message.author}',
                                         icon_url=ctx.author.avatar_url)
                        await msg.edit(embed=embed)
                elif str(reaction.emoji) == reacts[reactionIndex]:
                    everyPage = data[6 * (k - 1):k * 6]
                    editEmbed = discord.Embed(title=f"{everyPage[reactionIndex]['dungeon']}",
                                              url=f"{everyPage[reactionIndex]['link']}",
                                              description=f"{everyPage[reactionIndex]['description']}\n\nFor more information on the bosses, please react on the book!",
                                              colour=functions.embedColour(ctx.guild.id))
                    setList = ''
                    nameList = ''
                    for sets in everyPage[reactionIndex]['sets']:
                        setList += f'{sets}\n'
                    editEmbed.add_field(name='Sets', value=f"{setList}")
                    for names in everyPage[reactionIndex]['bosses']:
                        nameList += f'{names["name"]}\n'
                    editEmbed.set_image(url=f"{everyPage[reactionIndex]['image']}")
                    editEmbed.add_field(name='Bosses', value=f"{nameList}")
                    editEmbed.set_footer(text=f'Image from Elder Scrolls Online Wiki', icon_url=ctx.author.avatar_url)
                    await msg.edit(embed=editEmbed)
                    await msg.add_reaction('📖')
                elif str(reaction.emoji) == '📖':
                    everyPage = data[6 * (k - 1):k * 6]
                    bossesName = []
                    bossesMechanics = []
                    bossesStrategy = []
                    await msg.clear_reactions()
                    j = 0
                    for bossName in everyPage[reactionIndex]['bosses']:
                        bossesName.append(bossName['name'])
                        bossesMechanics.append(bossName['mechanics'])
                        bossesStrategy.append(bossName['strategy'])
                    mechanics = ''
                    strategies = ''
                    for mechanic in bossesMechanics[j]:
                        mechanics += f'{mechanic}\n'
                    for strategy in bossesStrategy[j]:
                        strategies += f'{strategy}\n'
                    if len(mechanics) < 1024 and len(strategies) < 1024:
                        bossEmbed = discord.Embed(title=f"{bossesName[j]}",
                                                  colour=functions.embedColour(ctx.guild.id))
                        bossEmbed.add_field(name='Mechanics', value=f'{mechanics}')
                        bossEmbed.add_field(name='Strategy', value=f'{strategies}')
                    elif len(strategies) < 1024 and not len(mechanics) < 1024:
                        bossEmbed = discord.Embed(title=f"{bossesName[j]}", description=f"**Mechanics**\n{mechanics}",
                                                  colour=functions.embedColour(ctx.guild.id))
                        bossEmbed.add_field(name='Strategy', value=f'{strategies}')
                    else:
                        bossEmbed = discord.Embed(title=f"{bossesName[j]}", description=f"**Strategy**\n{strategies}",
                                                  colour=functions.embedColour(ctx.guild.id))
                        bossEmbed.add_field(name='Mechanics', value=f'{mechanics}')
                    await msg.edit(embed=bossEmbed)
                    await msg.add_reaction('◀️')
                    await msg.add_reaction('▶️')
                    def check3(reaction, user):
                        return str(reaction.emoji) in ['◀️',
                                                       '▶️'] and user == ctx.message.author and reaction.message.id == msg.id
                    j = 0
                    async def handle_rotate3(reaction, msg, check, j):
                        await msg.remove_reaction(reaction, ctx.message.author)
                        if str(reaction.emoji) == '◀️':
                            j -= 1
                            try:
                                mechanics = ''
                                strategies = ''
                                for mechanic in bossesMechanics[j]:
                                    mechanics += f'{mechanic}\n'
                                for strategy in bossesStrategy[j]:
                                    strategies += f'{strategy}\n'
                                if len(mechanics) < 1024 and len(strategies) < 1024:
                                    bossEmbed = discord.Embed(title=f"{bossesName[j]}",
                                                              colour=functions.embedColour(ctx.guild.id))
                                    bossEmbed.add_field(name='Mechanics', value=f'{mechanics}')
                                    bossEmbed.add_field(name='Strategy', value=f'{strategies}')
                                elif len(strategies) < 1024 and not len(mechanics) < 1024:
                                    bossEmbed = discord.Embed(title=f"{bossesName[j]}",
                                                              description=f"**Mechanics**\n{mechanics}",
                                                              colour=functions.embedColour(ctx.guild.id))
                                    bossEmbed.add_field(name='Strategy', value=f'{strategies}')
                                else:
                                    bossEmbed = discord.Embed(title=f"{bossesName[j]}",
                                                              description=f"**Strategy**\n{strategies}",
                                                              colour=functions.embedColour(ctx.guild.id))
                                    bossEmbed.add_field(name='Mechanics', value=f'{mechanics}')
                                await msg.edit(embed=bossEmbed)
                            except IndexError:
                                embed = discord.Embed(
                                    description="You've reached the end of the pages! Press ◀️ to go back!")
                                await msg.edit(embed=embed)
                        elif str(reaction.emoji) == '▶️':
                            j += 1
                            try:
                                mechanics = ''
                                strategies = ''
                                for mechanic in bossesMechanics[j]:
                                    mechanics += f'{mechanic}\n'
                                for strategy in bossesStrategy[j]:
                                    strategies += f'{strategy}\n'
                                if len(mechanics) < 1024 and len(strategies) < 1024:
                                    bossEmbed = discord.Embed(title=f"{bossesName[j]}",
                                                              colour=functions.embedColour(ctx.guild.id))
                                    bossEmbed.add_field(name='Mechanics', value=f'{mechanics}')
                                    bossEmbed.add_field(name='Strategy', value=f'{strategies}')
                                elif len(strategies) < 1024 and not len(mechanics) < 1024:
                                    bossEmbed = discord.Embed(title=f"{bossesName[j]}",
                                                              description=f"**Mechanics**\n{mechanics}",
                                                              colour=functions.embedColour(ctx.guild.id))
                                    bossEmbed.add_field(name='Strategy', value=f'{strategies}')
                                else:
                                    bossEmbed = discord.Embed(title=f"{bossesName[j]}",
                                                              description=f"**Strategy**\n{strategies}",
                                                              colour=functions.embedColour(ctx.guild.id))
                                    bossEmbed.add_field(name='Mechanics', value=f'{mechanics}')
                                await msg.edit(embed=bossEmbed)
                            except IndexError:
                                embed = discord.Embed(
                                    description="You've reached the end of the pages! Press ◀️ to go back!")
                                await msg.edit(embed=embed)
                        else:
                            return
                        reaction, user = await self.bot.wait_for('reaction_add', check=check3)
                        await handle_rotate3(reaction, msg, check, j)
                    reaction, user = await self.bot.wait_for('reaction_add', check=check3)
                    await handle_rotate3(reaction, msg, check, j)
                reaction, user = await self.bot.wait_for('reaction_add', check=check)
                await handle_rotate(reaction, msg, check, k)
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
            await handle_rotate(reaction, msg, check, k)
        elif dungeon:
            dungeonsList = []
            for d in data:
                dungeonsList.append(d['dungeon'])
            inputIndex = dungeonsList.index(dungeon)
            if dungeon not in dungeonsList:
                await functions.requestEmbedTemplate(ctx,
                                                     f"The dungeon name you've entered does not exist! Please check your spelling (case sensitive).",
                                                     ctx.message.author)
                return
            embed = discord.Embed(title=f"{data[inputIndex]['dungeon']}",
                                  url=f"{data[inputIndex]['link']}",
                                  description=f"{data[inputIndex]['description']}\n\nFor more information on the bosses, please react on the book!",
                                  colour=functions.embedColour(ctx.guild.id))
            setList = ''
            nameList = ''
            for sets in data[inputIndex]['sets']:
                setList += f'{sets}\n'
            embed.add_field(name='Sets', value=f"{setList}")
            for names in data[inputIndex]['bosses']:
                nameList += f'{names["name"]}\n'
            embed.set_image(url=f"{data[inputIndex]['image']}")
            embed.add_field(name='Bosses', value=f"{nameList}")
            embed.set_footer(text=f'Image from Elder Scrolls Online Wiki', icon_url=ctx.author.avatar_url)
            msg = await ctx.send(embed=embed)
            await msg.add_reaction('📖')
            def check(reaction, user):
                return str(reaction.emoji) in ['📖'] and user == ctx.message.author and reaction.message.id == msg.id
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
            if str(reaction.emoji) == '📖':
                bossesName = []
                bossesMechanics = []
                bossesStrategy = []
                await msg.clear_reactions()
                j = 0
                for bossName in data[inputIndex]['bosses']:
                    bossesName.append(bossName['name'])
                    bossesMechanics.append(bossName['mechanics'])
                    bossesStrategy.append(bossName['strategy'])
                mechanics = ''
                strategies = ''
                for mechanic in bossesMechanics[j]:
                    mechanics += f'{mechanic}\n'
                for strategy in bossesStrategy[j]:
                    strategies += f'{strategy}\n'
                if len(mechanics) < 1024 and len(strategies) < 1024:
                    bossEmbed = discord.Embed(title=f"{bossesName[j]}",
                                              colour=functions.embedColour(ctx.guild.id))
                    bossEmbed.add_field(name='Mechanics', value=f'{mechanics}')
                    bossEmbed.add_field(name='Strategy', value=f'{strategies}')
                elif len(strategies) < 1024 and not len(mechanics) < 1024:
                    bossEmbed = discord.Embed(title=f"{bossesName[j]}", description=f"**Mechanics**\n{mechanics}",
                                              colour=functions.embedColour(ctx.guild.id))
                    bossEmbed.add_field(name='Strategy', value=f'{strategies}')
                else:
                    bossEmbed = discord.Embed(title=f"{bossesName[j]}", description=f"**Strategy**\n{strategies}",
                                              colour=functions.embedColour(ctx.guild.id))
                    bossEmbed.add_field(name='Mechanics', value=f'{mechanics}')
                await msg.edit(embed=bossEmbed)
                await msg.add_reaction('◀️')
                await msg.add_reaction('▶️')
                def check3(reaction, user):
                    return str(reaction.emoji) in ['◀️',
                                                   '▶️'] and user == ctx.message.author and reaction.message.id == msg.id
                j = 0
                async def handle_rotate3(reaction, msg, check, j):
                    await msg.remove_reaction(reaction, ctx.message.author)
                    if str(reaction.emoji) == '◀️':
                        j -= 1
                        try:
                            mechanics = ''
                            strategies = ''
                            for mechanic in bossesMechanics[j]:
                                mechanics += f'{mechanic}\n'
                            for strategy in bossesStrategy[j]:
                                strategies += f'{strategy}\n'
                            if len(mechanics) < 1024 and len(strategies) < 1024:
                                bossEmbed = discord.Embed(title=f"{bossesName[j]}",
                                                          colour=functions.embedColour(ctx.guild.id))
                                bossEmbed.add_field(name='Mechanics', value=f'{mechanics}')
                                bossEmbed.add_field(name='Strategy', value=f'{strategies}')
                            elif len(strategies) < 1024 and not len(mechanics) < 1024:
                                bossEmbed = discord.Embed(title=f"{bossesName[j]}",
                                                          description=f"**Mechanics**\n{mechanics}",
                                                          colour=functions.embedColour(ctx.guild.id))
                                bossEmbed.add_field(name='Strategy', value=f'{strategies}')
                            else:
                                bossEmbed = discord.Embed(title=f"{bossesName[j]}",
                                                          description=f"**Strategy**\n{strategies}",
                                                          colour=functions.embedColour(ctx.guild.id))
                                bossEmbed.add_field(name='Mechanics', value=f'{mechanics}')
                            await msg.edit(embed=bossEmbed)
                        except IndexError:
                            embed = discord.Embed(
                                description="You've reached the end of the pages! Press ◀️ to go back!")
                            await msg.edit(embed=embed)
                    elif str(reaction.emoji) == '▶️':
                        j += 1
                        try:
                            mechanics = ''
                            strategies = ''
                            for mechanic in bossesMechanics[j]:
                                mechanics += f'{mechanic}\n'
                            for strategy in bossesStrategy[j]:
                                strategies += f'{strategy}\n'
                            if len(mechanics) < 1024 and len(strategies) < 1024:
                                bossEmbed = discord.Embed(title=f"{bossesName[j]}",
                                                          colour=functions.embedColour(ctx.guild.id))
                                bossEmbed.add_field(name='Mechanics', value=f'{mechanics}')
                                bossEmbed.add_field(name='Strategy', value=f'{strategies}')
                            elif len(strategies) < 1024 and not len(mechanics) < 1024:
                                bossEmbed = discord.Embed(title=f"{bossesName[j]}",
                                                          description=f"**Mechanics**\n{mechanics}",
                                                          colour=functions.embedColour(ctx.guild.id))
                                bossEmbed.add_field(name='Strategy', value=f'{strategies}')
                            else:
                                bossEmbed = discord.Embed(title=f"{bossesName[j]}",
                                                          description=f"**Strategy**\n{strategies}",
                                                          colour=functions.embedColour(ctx.guild.id))
                                bossEmbed.add_field(name='Mechanics', value=f'{mechanics}')
                            await msg.edit(embed=bossEmbed)
                        except IndexError:
                            embed = discord.Embed(
                                description="You've reached the end of the pages! Press ◀️ to go back!")
                            await msg.edit(embed=embed)
                    else:
                        return
                    reaction, user = await self.bot.wait_for('reaction_add', check=check3)
                    await handle_rotate3(reaction, msg, check, j)
                reaction, user = await self.bot.wait_for('reaction_add', check=check3)
                await handle_rotate3(reaction, msg, check, j)

    @command(description="`!set {set}`\n\nDisplays information on a specific set.")
    async def set(self, ctx, *set):
        """
        Lookup information on any set.
        """
        await command_invoked(self.bot, "set", ctx.author.name)
        with open("assets/sets.json", "r", encoding="utf-8") as dungeons:
            data = json.load(dungeons)
        result = False
        set_ = " ".join(set)
        if len(set_) < 3:
            return await ctx.send("Your search request must be at least 3 characters.")
        for x in data:
            if set_.lower() == x["name"].lower():
                result = True
                embed = discord.Embed(
                    title=x["name"],
                    description=x["effects"],
                    url=x["link"],
                    colour=functions.embedColour(ctx.guild.id),
                )
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
                return await ctx.invoke(self.set, reference_sets[0])
            elif len(reference_sets) > 0:
                loaded_sets = reference_sets
            elif len(reference_sets) == 0:
                return await ctx.send(
                    f"No results were found matching your request: `{set_}`"
                )
            else:
                loaded_sets = [x["name"] for x in data]
            for index, x in enumerate(loaded_sets):
                results += f"`{index + 1}` {x} \n"
            embed = discord.Embed(
                title="Sets",
                description=f"`{set_}` was not found.\nDid you mean one of the following "
                f"sets:\n{results}\nReply "
                f"with a number for more information.",
                colour=functions.embedColour(ctx.guild.id),
                timestamp=time,
            )
            await ctx.send(embed=embed)

            def check(m):
                return (
                    m.content in [str(i) for i in range(1, len(loaded_sets) + 1)]
                    and m.channel == ctx.channel
                    and ctx.author == m.author
                )

            try:
                choice = await ctx.bot.wait_for("message", timeout=10.0, check=check)
            except asyncio.TimeoutError:
                return await ctx.send("Request timed out.")
            if choice:
                set = f"{loaded_sets[int(choice.content) - 1].lower()}"
                await ctx.send(f"!set {set}")
                async with ctx.typing():
                    return await ctx.invoke(self.set, set)

    @command(description="`!skill {skill}`\n\nDisplays information on a specific skill.")
    async def skill(self, ctx, *skill):
        """
        Lookup information on any skill.
        """
        await command_invoked(self.bot, "skill", ctx.author.name)
        with open("assets/skills.json", "r", encoding="utf-8") as dungeons:
            data = json.load(dungeons)
        result = False
        skill = " ".join(skill)
        if len(skill) < 3:
            return await ctx.send("Your search request must be at least 3 characters.")
        for x in data:
            if skill.lower() == x["name"].lower():
                result = True
                embed = discord.Embed(
                    title=x["name"],
                    description=x["effect"],
                    url=x["link"],
                    colour=functions.embedColour(ctx.guild.id),
                )
                embed.set_thumbnail(url=x["image"])
                embed.set_footer(text="Skills and icons © by ZeniMax Online Studios")
                return await ctx.send(embed=embed)
        if result is False:
            reference_skills = []
            results = ""
            timezone = pytz.timezone("Europe/Amsterdam")
            time = timezone.localize(datetime.datetime.now())
            for x in data:
                if skill.lower() in x["name"].lower():
                    reference_skills.append(x["name"])
            if len(reference_skills) == 1:
                return await ctx.invoke(self.set, reference_skills[0])
            elif len(reference_skills) > 0:
                loaded_sets = reference_skills
            elif len(reference_skills) == 0:
                return await ctx.send(
                    f"No results were found matching your request: `{skill}`"
                )
            else:
                loaded_sets = [x["name"] for x in data]
            for index, x in enumerate(loaded_sets):
                results += f"`{index + 1}` {x} \n"
            embed = discord.Embed(
                title="Sets",
                description=f"`{skill}` was not found.\nDid you mean one of the following "
                            f"skills:\n{results}\nReply "
                            f"with a number for more information.",
                colour=functions.embedColour(ctx.guild.id),
                timestamp=time,
            )
            await ctx.send(embed=embed)

            def check(m):
                return (
                        m.content in [str(i) for i in range(1, len(loaded_sets) + 1)]
                        and m.channel == ctx.channel
                        and ctx.author == m.author
                )
            try:
                choice = await ctx.bot.wait_for("message", timeout=10.0, check=check)
            except asyncio.TimeoutError:
                return await ctx.send("Request timed out.")
            if choice:
                skill = f"{loaded_sets[int(choice.content) - 1].lower()}"
                await ctx.send(f"!skill {skill}")
                async with ctx.typing():
                    return await ctx.invoke(self.skill, skill)

    @command(name="class", description="`!class {class}`\n\nDisplays information on a specific class.")
    async def class_command(self, ctx, *class_):
        """
        Lookup information on any class.
        """
        await command_invoked(self.bot, "skill", ctx.author.name)
        with open("assets/classes.json", "r", encoding="utf-8") as dungeons:
            data = json.load(dungeons)
        result = False
        class_ = " ".join(class_)
        if len(class_) < 3:
            return await ctx.send("Your search request must be at least 3 characters.")
        for x in data:
            if class_.lower() == x["name"].lower():
                result = True
                embed = discord.Embed(
                    title=x["name"],
                    description=x["about"],
                    url=x["link"],
                    colour=functions.embedColour(ctx.guild.id),
                )
                skills = ""
                for skill in x["skills"]:
                    skills += f"[{skill['name']}]({skill['link']})\n{skill['description']}\n"
                embed.add_field(name="Skills", value=skills)
                embed.set_thumbnail(url=x["image"])
                embed.set_footer(text="Classes and icons © by ZeniMax Online Studios")
                return await ctx.send(embed=embed)
        if result is False:
            reference_classes = []
            results = ""
            timezone = pytz.timezone("Europe/Amsterdam")
            time = timezone.localize(datetime.datetime.now())
            for x in data:
                if class_.lower() in x["name"].lower():
                    reference_classes.append(x["name"])
            if len(reference_classes) == 1:
                return await ctx.invoke(self.class_command, reference_classes[0])
            elif len(reference_classes) > 0:
                loaded_sets = reference_classes
            elif len(reference_classes) == 0:
                return await ctx.send(
                    f"No results were found matching your request: `{class_}`"
                )
            else:
                loaded_sets = [x["name"] for x in data]
            for index, x in enumerate(loaded_sets):
                results += f"`{index + 1}` {x} \n"
            embed = discord.Embed(
                title="Sets",
                description=f"`{class_}` was not found.\nDid you mean one of the following "
                            f"classes:\n{results}\nReply "
                            f"with a number for more information.",
                colour=functions.embedColour(ctx.guild.id),
                timestamp=time,
            )
            await ctx.send(embed=embed)

            def check(m):
                return (
                        m.content in [str(i) for i in range(1, len(loaded_sets) + 1)]
                        and m.channel == ctx.channel
                        and ctx.author == m.author
                )

            try:
                choice = await ctx.bot.wait_for("message", timeout=10.0, check=check)
            except asyncio.TimeoutError:
                return await ctx.send("Request timed out.")
            if choice:
                class_ = f"{loaded_sets[int(choice.content) - 1].lower()}"
                await ctx.send(f"!skill {class_}")
                async with ctx.typing():
                    return await ctx.invoke(self.class_command, class_)


def setup(bot):
    bot.add_cog(Lookup(bot))
