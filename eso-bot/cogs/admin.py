from backend.helpers import command_invoked

from discord.ext.commands import Cog, command


class Admin(Cog, name='Admin commands'):
    """
    Admin commands.
    """
    def __init__(self, bot):
        self.bot = bot
        self.admins = [391583287652515841]

    @command(name="stop")
    async def restart_command(self, ctx):
        await command_invoked(self.bot, "stop", ctx.message.author)
        user = ctx.message.author.id
        if user in self.admins:
            await ctx.send("Goodbye cruel world :(")
            return await self.bot.logout()
        else:
            return await ctx.send("Only admins can use that command.")


def setup(bot):
    bot.add_cog(Admin(bot))
