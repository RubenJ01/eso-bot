import discord

from discord.ext.commands import Bot
from discord import Activity, ActivityType

bot = Bot(
    activity=Activity(
        name="Im online!",
        type=ActivityType.watching
    ),
    command_prefix="!",
    pm_help=True
)

extensions = ['cogs.dungeon']

bot.remove_command('help')


@bot.event
async def on_command_error(ctx, error):
    return await ctx.send(f"Something seems to have gone wrong oops... ```{error}```")


def main():
    """Load cogs, configuration, and start the bot."""
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except:
            print(f"could not load {extension}")

    bot.run("NTcyMzY1NzQ5NzgwMzQ4OTI4.XMbPJA.-59DN6IT6eE9HhfvvhjxmvvToAI")


if __name__ == "__main__":
    main()
