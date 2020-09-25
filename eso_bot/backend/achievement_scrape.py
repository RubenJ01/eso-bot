import requests
import json
from pathlib import Path

from bs4 import BeautifulSoup

urls = [
    "http://esoitem.uesp.net/viewlog.php?start=0&record=achievements",
    "http://esoitem.uesp.net/viewlog.php?start=500&record=achievements",
    "http://esoitem.uesp.net/viewlog.php?start=1000&record=achievements",
    "http://esoitem.uesp.net/viewlog.php?start=1500&record=achievements",
    "http://esoitem.uesp.net/viewlog.php?start=2000&record=achievements",
]

achievements = []
for url in urls:
    response = requests.get(url).text
    soup = BeautifulSoup(response, "lxml")
    table = soup.find("table")
    table_rows = table.find_all_next("tr")[1:]
    for tr in table_rows:
        td = tr.find_all_next("td")
        achievement = {
            "name": str(td[2].text),
            "description": str(td[3].text),
            "points": int(td[8].text),
            "image": str(td[9].find("img").get("src").replace("//", "https://")),
        }
        achievements.append(achievement)


achievements_file = Path("achievements.json")

with achievements_file.open("w") as f:
    json.dump(achievements, f, indent=4)
