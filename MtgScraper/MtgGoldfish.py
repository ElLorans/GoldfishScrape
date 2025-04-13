from bs4 import BeautifulSoup

from MtgScraper.base import MtgScraper, FormatNameLower
from MtgScraper.mtg_utils import UNCLEAR_DECK_NAMES, MtgBoard, MtgDeck


class MtgGoldfishScraper(MtgScraper):
    base_url = "https://www.mtggoldfish.com/metagame/"
    allowed_formats: set[FormatNameLower] = {'standard', 'modern', 'pioneer', 'historic', 'explorer', 'timeless',
                                             'alchemy', 'pauper', 'legacy', 'vintage', 'penny dreadful',
                                             'duel commander', 'commander', 'brawl'}

    def translate_format_name(self, string: str) -> str:
        return string.lower().replace(' ', '_')

    def build_url_format(self, formato: str) -> str:
        url_end: str = "/full#paper" if self.fullness else "/#paper"
        # weird bug on Pauper requiring lower case. Browsers not affected, but requests is.
        formato = formato.lower()
        correct_names = {"commander_1v1": "duel_commander"}
        formato = correct_names.get(formato, formato)
        return self.base_url + formato + url_end

    def fetch_all_links(self, soup: BeautifulSoup) -> dict[str, str]:
        names = soup.find_all('span', {'class': 'deck-price-paper'})[1:]
        names_links: dict[str, str] = {}
        for elem in names:
            if not elem.a:  # not a real deck
                continue
            name = elem.text.replace('\n', '')
            if name not in names_links and name != 'Other':
                # if deck name already present do NOT insert it in result dict
                if self.clean and name in UNCLEAR_DECK_NAMES:  # exclude decks with bad names
                    pass
                else:
                    names_links[name] = "https://www.mtggoldfish.com" + elem.a["href"]
        return names_links

    def scrape_page(self, url: str) -> MtgDeck:
        soup = self.get_soup(url)
        if not soup:
            breakpoint()
            return MtgDeck()
        deck_plain_text = soup.find('input', {'id': "deck_input_deck"})['value']
        splitted_deck = deck_plain_text.split('sideboard')
        main_text = splitted_deck[0]
        if len(splitted_deck) > 1:
            side_text = splitted_deck[1]
            return MtgDeck(MtgBoard.from_text(main_text), MtgBoard.from_text(side_text))
        return MtgDeck(MtgBoard.from_text(main_text), None)


if __name__ == '__main__':
    example_deck = "https://www.mtggoldfish.com/archetype/legacy-dimir-tempo#paper"
    deck = MtgGoldfishScraper().scrape_page(example_deck)
    print(deck)
