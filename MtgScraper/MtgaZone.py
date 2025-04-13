from typing import Optional, Tuple, Iterable, Any

import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

from MtgScraper.base import MtgScraper, FormatNameLower
from MtgScraper.mtg_utils import MtgDeck, MtgBoard


class MtgaZoneScraper(MtgScraper):
    #TODO: tier lists are easy, formats are more complex
    base_url = "https://mtgazone.com/"
    allowed_formats: set[FormatNameLower] = {"standard", "timeless", "historic"}

    def translate_format_name(self, string: str) -> str:
        return string.lower()

    def build_url_format(self, formato: str) -> str:
        standard_url = 'https://mtgazone.com/standard-bo3-metagame-tier-list/'
        historic_url = 'https://mtgazone.com/historic-bo3-metagame-tier-list/'
        timeless_url = 'https://mtgazone.com/timeless-bo3-metagame-tier-list/'

        formats_to_url: dict[str, str] = {'standard': standard_url, 'historic': historic_url,
                                          'timeless': timeless_url}
        return formats_to_url[formato.lower()]

    def fetch_all_links(self, soup: BeautifulSoup) -> dict[str, str]:
        return {"All decks": soup}

    def scrape_page(self, url: str) -> MtgDeck:
        raise NotImplementedError("More complex code and not needed RN. TODO later")

    def scrape_format(self, formato: str, **params: dict[str, Any]) -> dict[str, MtgDeck]:
        soup = self.get_soup(self.build_url_format(formato), **params)
        if not soup:
            breakpoint()
            return {}
        decks = soup.find_all("div", {"class": "deck-block"})
        result: dict[str, MtgDeck] = {}
        for deck in tqdm(decks, position=0, leave=True):
            name = deck.find("div", {"class": "name"}).text.strip()
            main_soup = deck.find("div", {"class": "decklist main"})
            side_soup = deck.find("div", {"class": "decklist sideboard"})
            deck = MtgDeck()
            for i, board_soup in enumerate((main_soup, side_soup)):
                board = MtgBoard()
                if board_soup:
                    cards = board_soup.find_all("div", {"class": "card"})
                    for card in cards:
                        board[card["data-name"]] = int(card["data-quantity"])
                deck[i] = board
            result[name] = deck
        return result

if __name__ == "__main__":
    scraper = MtgaZoneScraper()
    std_decks = scraper.scrape_format("standard")
    print(std_decks)
    breakpoint()
