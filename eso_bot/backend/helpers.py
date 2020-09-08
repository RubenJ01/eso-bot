import discord
import pytz
import datetime
from pathlib import Path

from bs4 import BeautifulSoup
from bs4.element import Tag


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
    embed = discord.Embed(
        title="Command invoked",
        description=f"`!{name}` was used by `{user}`",
        timestamp=time,
    )
    return await logging_channel.send(embed=embed)


def scrape_all_sets() -> list:
    """
    Scrapes all set of the eso-sets website.
    :return: list with each set in a dict
    """
    sets: list = []
    p = Path("source.html")  # html of the source page
    soup = BeautifulSoup(p.read_text(), "lxml")
    table_body: Tag = soup.find("tbody")
    table_rows: list = table_body.find_all("tr")
    for row in table_rows:
        set_link = row.find("a").get("href")
        set_name = (
            set_link.replace("https://eso-sets.com/set/", "").replace("-", " ").title()
        )
        image_link = row.find("img").get("src")
        set_effects = row.find_all("td")[-1].text.strip()
        set_ = {
            "name": set_name,
            "link": set_link,
            "image": image_link,
            "effects": set_effects,
        }
        sets.append(set_)
    return sets
