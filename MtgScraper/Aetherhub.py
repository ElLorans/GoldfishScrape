# Scrape brawl from Aetherhub
from bs4 import BeautifulSoup

from MtgScraper.base import MtgScraper, FormatNameLower
from MtgScraper.mtg_utils import MtgDeck, MtgBoard


class AetherhubScraper(MtgScraper):
    base_url = "https://aetherhub.com"
    allowed_formats: set[FormatNameLower] = {"standard", "timeless", "historic", "historic brawl"}

    def translate_format_name(self, string: str) -> str:
        return string.replace("_", " ").title()

    def build_url_format(self, formato: str) -> str:
        # _ in url will cause 200 but showing Standard page.
        # e.g.: https://aetherhub.com/Metagame/Historic_Brawl gives Standard decks
        string = self.translate_format_name(formato)
        return f'https://aetherhub.com/Metagame/{string}/'

    def fetch_all_links(self, soup: BeautifulSoup) -> dict[str, str]:
        decks_html = soup.find_all('td', {'class': 'ae-decktitle'})
        return {el.text.strip(): 'https://aetherhub.com' + el.find('a')['href'] for el in decks_html}

    def scrape_page(self, url: str) -> MtgDeck:
        soup = self.get_soup(url)
        if not soup:
            return MtgDeck()
        tables = soup.find_all('table', {'class': 'table'})
        if len(tables) > 1:  # decks can have only main
            tables = tables[0:2]
        deck = MtgDeck()
        for i, table in enumerate(tables):
            board = MtgBoard()
            cards = table.find_all('div', {'class': 'hover-imglink'})
            for card in cards:
                text: list[str] = card.text.split()  # split removes whitespace \n\r and "     "
                copies, card = int(text[0]), " ".join(text[1:])
                board[card] = copies
            deck[i] = board

        if deck.mainboard.count() < 40:
            # we scraped Brawl/Commander and first table was only commander
            # return Union of Commander and mainboard. Sideboard is always None since it is not allowed by Mtg rules
            return MtgDeck(MtgBoard(**deck.mainboard, **deck.sideboard), None)
        return deck


if __name__ == "__main__":
    scraper = AetherhubScraper()
    # std = scraper.scrape_format("Standard")
    # brawl = scraper.scrape_format("Brawl")
    brawl_deck = scraper.scrape_page("https://aetherhub.com/Metagame/Brawl/Deck/bristly-bill-spine-sower-1164422")
    print(brawl_deck)
    breakpoint()
