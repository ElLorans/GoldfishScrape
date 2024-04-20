from __future__ import annotations

from dataclasses import dataclass
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm


@dataclass
class DeckInfo:
    rank: str
    name: str
    url: str
    player: str
    decklist: str


def get_links(soup: BeautifulSoup) -> list[DeckInfo]:
    decks_infos = []
    hyperlinks = soup.find_all("div", class_=("hover_tr",
                                              # "chosen_tr",   # get link of current deck, too
                                              )
                               )
    for i, deck in tqdm(
            enumerate(
                hyperlinks
            )
    ):
        # i can be max 7 if current deck is excluded, or 8 if current deck is included
        # do not include first card in deck
        if "deck_line" in deck.__dict__["attrs"]["class"] or i >= 8:
            break
        try:
            rank, deck_name = deck.find_all("div", class_="S14")
            deck_info = DeckInfo(
                rank=rank.text,
                name=deck_name.text,
                url="https://www.mtgtop8.com/event" + deck_name.find("a")["href"],
                player=deck.find("div", class_="G11").text,
                decklist="",
            )
            decks_infos.append(deck_info)
        except ValueError as e:
            print(e)
            breakpoint()
    return decks_infos


def get_decklist(soup: BeautifulSoup) -> list[str, ...]:
    decklist = []
    deck_text = soup.find("div", attrs={'style': "display:flex;align-content:stretch;"})
    try:
        for col in deck_text:
            for el in col:
                decklist.append(el.text.strip())
    except TypeError:
        print("Decklist not found")
    return decklist


class MtgTop8Scraper:
    def __init__(self, session=None):
        if session is None:
            self.session = requests.Session()
        else:
            self.session = session

    def scrape_event(self, url: str):
        with self.session as s:
            response = s.get(url)
            soup = BeautifulSoup(response.content, "lxml")
            links: list[DeckInfo] = get_links(soup)
            decklists = [get_decklist(soup)]
            for link in tqdm(links):
                new_response = s.get(link.url)
                new_soup = BeautifulSoup(new_response.content, "lxml")
                new_decklist = get_decklist(new_soup)
                decklists.append(new_decklist)
        return decklists


if __name__ == "__main__":
    scraper = MtgTop8Scraper()
    lists = scraper.scrape_event("https://www.mtgtop8.com/event?e=40809&f=MO")
    pprint(lists)
    breakpoint()
