import requests
import json
from pathlib import Path

from bs4 import BeautifulSoup

urls = ["https://esoitem.uesp.net/viewlog.php?record=cpSkills"]

champion_skills = []
for url in urls:
    response = requests.get(url).text
    soup = BeautifulSoup(response, "lxml")
    table = soup.find("table")
    table_rows = table.find_all_next("tr")[1:]
    for tr in table_rows:
        td = tr.find_all_next("td")
        champoin_skill = {
            "name": td[6].text,
            "unlock_level": td[5].text,
            "max_level": td[7].text,
            "min_stats": td[8].text,
            "max_stats": td[9].text,
        }
        champion_skills.append(champoin_skill)


achievements_file = Path("champion_skills.json")

with achievements_file.open("w") as f:
    json.dump(champion_skills, f, indent=4)
