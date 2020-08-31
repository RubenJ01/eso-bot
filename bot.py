import discord
import datetime
import pytz

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

extensions = ['cogs.dungeon', 'cogs.admin']

bot.remove_command('help')


@bot.event
async def on_ready():
    print("Bot sucessfully started.")
    logging_channel = bot.get_channel(749940498885509190)
    timezone = pytz.timezone("Europe/Amsterdam")
    time = timezone.localize(datetime.datetime.now())
    embed = discord.Embed(title="on_ready()", description="Bot succesfully started.", timestamp=time)
    return await logging_channel.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    logging_channel = bot.get_channel(749940498885509190)
    timezone = pytz.timezone("Europe/Amsterdam")
    time = timezone.localize(datetime.datetime.now())
    embed = discord.Embed(title="on_command_error()", description=f"`{error}`", timestamp=time)
    await ctx.send(f"Sorry something went wrong.")
    return await logging_channel.send(embed=embed)


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
