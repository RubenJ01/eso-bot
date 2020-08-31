import discord
import pytz
import datetime


async def command_invoked(bot, name, user):
    """
    Adds the invoked command to the logs.
    :param bot:
    :param name: the name of the invoked command
    :param user: the user that invoked the command
    :return: sends a log of the invoked command to the logging channel.
    """
    logging_channel = bot.get_channel(749940498885509190)
    timezone = pytz.timezone("Europe/Amsterdam")
    time = timezone.localize(datetime.datetime.now())
    embed = discord.Embed(title="Command invoked", description=f"`!{name}` was used by `{user}`", timestamp=time)
    return await logging_channel.send(embed=embed)
