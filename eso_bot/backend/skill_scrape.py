from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag


def fetch_data(url: str) -> str:
    """GET webpage source/HTML for skill."""
    response = requests.get(url)

    if response.status_code != 200:
        return None

    # example -> content_type = "text/html; charset=UTF-8"
    content_type: str = response.headers["content-type"]

    charset: str = content_type.split(";")[1].strip().split("=")[1].lower()

    # response.content is of the type `bytes`.
    # convert bytes to string (byte sequence).
    return response.content.decode(charset)


def process_data(html_content: str, url: str) -> dict:
    """Process HTML for skill dict."""
    try:
        soup = BeautifulSoup(html_content, "lxml")
    except Exception as e:
        print(str(e))
        return {}

    info_container: Tag = soup.find("div", class_="set-tooltip-center")

    skill_name: str = info_container.find("h4").text
    skill_image_link: str = info_container.find("img")["src"]

    spans: List[Tag] = info_container.find_all("span")

    for span in spans:
        if span.text.startswith("Skill") and span.find("strong"):
            span_text: str = span.text.lower()
            starting_text: str = "skill description"
            start_index: int = span_text.index(starting_text) + len(starting_text)

            effect: str = (
                span_text[start_index:].strip().capitalize()
            )  # skill description

    skill: dict = {
        "name": skill_name,
        "effect": effect,
        "link": url,
        "image": skill_image_link,
    }

    return skill


def generate_skill_dict(skill_name: str) -> Optional[dict]:
    skill_name = skill_name.lower().replace(" ", "-")
    url: str = f"https://eso-skillbook.com/skill/{skill_name.lower()}"
    skill_webpage_html: str = fetch_data(url)
    if not skill_webpage_html:
        return None
    skill_dict: dict = process_data(skill_webpage_html, url)
    return skill_dict
