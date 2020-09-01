from backend.helpers import command_invoked

from backend.helpers import command_invoked

from discord import Colour, Embed
from discord.ext import buttons
from discord.ext.commands import Cog, command


class Paginator(buttons.Paginator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Misc(Cog, name='Misc commands'):
    """
    Miscellaneous commands.
    """
    def __init__(self, bot):
        self.bot = bot
        self.invite_link = "https://discord.com/oauth2/authorize?client_id=572365749780348928&permissions=0&scope=bot"

    @command(name="invite")
    async def invite_command(self, ctx):
        """
        Get an invite link for the bot.
        """
        await command_invoked(self.bot, "invite", ctx.author.name)
        return await ctx.send(self.invite_link)

    @command(name='help')
    async def help_(self, ctx, second_help: str = None):
        """
        Get a list of all the bot commands.
        """
        await command_invoked(self.bot, "help", ctx.author.name)
        cogs = sorted([cog for cog in self.bot.cogs.keys() if cog not in ['Admin commands']])
        pages = []
        page = 1
        cmd_names = [cmd.name for cmd in self.bot.commands]
        if not second_help:
            for cog_name in cogs:
                cog = self.bot.get_cog(cog_name)
                commands = [cmd for cmd in cog.get_commands() if not cmd.hidden or cmd.name == 'help']
                message = cog.description + '\n'
                for cmd in commands:
                    message += f' \n  **!{cmd}** \n *{cmd.help}*'
                help_embed = Embed(title=cog_name, colour=Colour.blurple(), description=message)
                help_embed.set_footer(text=f'Page: {page}/{len(cogs)}')
                help_embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar_url)
                pages.append(help_embed)
                page = page + 1
            embed = Paginator(embed=False, timeout=90, use_defaults=True,
                              extra_pages=pages, length=1)
            await embed.start(ctx)
        else:
            if second_help.lower() in cmd_names:
                cmd = self.bot.get_command(second_help)
                embed = Embed(title=cmd.name, colour=Colour.blurple())
                value = ''
                if cmd.aliases:
                    for alias in cmd.aliases:
                        value += f'{str(alias)}, '
                    value = value[0:-2]
                    value = value + '.'
                else:
                    value = None
                embed.add_field(name="Aliases", value=f'*{value}*', inline=False)
                params_list = list(cmd.params.keys())
                req_params = []
                for value in params_list:
                    req_params.append(value)
                req_params.remove('self')
                req_params.remove('ctx')
                param_message = 'Required parameters are:\n**'
                if req_params:
                    for parm in req_params:
                        param_message += parm + '\n'
                    embed.add_field(name='Usage', value=param_message + '**', inline=False)
                else:
                    embed.add_field(name='Usage', value=param_message + 'None**', inline=False)
                embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)
            else:
                return await ctx.send(f"{str(second_help)} command does not exist!")


def setup(bot):
    bot.add_cog(Misc(bot))
