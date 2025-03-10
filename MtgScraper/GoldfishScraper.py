"""
Download all Goldfish decks in a dictionary.

main()
    grab_links()
    scrape_deck_page()
        scrape_cards()
            deck_text_to_dict()
"""
import logging
from typing import Dict, Iterable, Optional, Tuple, Union

import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

from MtgScraper.mtg_utils import *


def grab_links(gf_html: str, clean: bool = True) -> Dict[str, str]:
    """
    Return ORDERED dict of links to scrape; if param clean is True, decks named only after colours combinations are
        not included.
    :param gf_html: html page of goldfish metagame page for a specific format (can be full or partial page)
                          e.g.: https://www.mtggoldfish.com/metagame/modern/full#paper
    :param clean: True or anything else: if clean is not True, decks names like R, UW, etc. are not
                  scraped
    :return: dictionary of deck_names with their links {deck_name: deck_relative_link, ...}
    """
    if clean:
        logging.info("WATCH OUT: decks with names such as WR and WRBG will not be scraped")

    # split at View More to avoid Budget Decks if program is scraping only partial page
    non_budget = gf_html.split("View More")[0]
    soup = BeautifulSoup(non_budget, "lxml")
    names = soup.find_all('span', {'class': 'deck-price-paper'})[1:]
    names_links: Dict[str, str] = dict()

    for elem in names:
        name = elem.text.replace('\n', '')

        if name not in names_links and name != 'Other':
            # if deck name already present do NOT insert it in result dict
            if clean and name not in unclear_deck_names:  # exclude decks with bad names
                names_links[name] = "https://www.mtggoldfish.com" + elem.a["href"]

            elif not clean:
                names_links[name] = "https://www.mtggoldfish.com" + elem.a["href"]
    return names_links


def scrape_cards(html_soup: BeautifulSoup) -> Tuple[MtgBoard, Optional[MtgBoard]]:
    """
    Scrape cards in deck list page.
    :param html_soup: BeautifulSoup of html deck page OF both mainboard or sideboard
    :return: tuple of dictionaries of deck cards ({"Mox Opal": 4, ...}, {"Galvanic Blast": 2, ...})
    """
    deck_plain_text = html_soup.find('input', {'id': "deck_input_deck"})['value']
    splitted_deck = deck_plain_text.split('sideboard')
    main_text = splitted_deck[0]
    if len(splitted_deck) > 1:
        side_text = splitted_deck[1]
        return deck_text_to_dict(main_text), deck_text_to_dict(side_text)
    return deck_text_to_dict(main_text), None


def scrape_deck_page(html_deck: str, deck_name: Optional[str] = None) -> (str, MtgBoard, MtgBoard):
    """
    Get Tuple with Deck Name, Mainboard dict and Sideboard dict from html of deck page.
    TODO: Improve Deck Name (unreliable since Nov 2020)
    :param html_deck: html page of deck e.g.: https://www.mtggoldfish.com/archetype/standard-jeskai-fires#paper
    :param deck_name:
    :return: tuple (deck_name: str, mainboard: dict, sideboard: dict)
    """
    soup = BeautifulSoup(html_deck, "lxml")

    # find author, then get parent node. Easiest way I could find to exclude author from deck name.
    # Structure:
    # <h1 class ="title">
    #   Four - Color Omnath
    #   <span class ="author"> by VTCLA </span>
    # </h1>
    if deck_name is None:
        deck_name = soup.find("span", {"class": "author"}).previousSibling.replace('\n', '').strip()
        deck_name = deck_name.replace("/", "").replace("-", " ").replace("\n\nSuggest\xa0a\xa0Better\xa0Name",
                                                                         "").replace("\nFix Archetype", "")

        for sign in ("[", "<", "{"):
            deck_name = deck_name.split(sign)[0]
    main, side = scrape_cards(soup)
    return deck_name, main, side


def build_url(formato: str, full: bool = True):
    url_start = "https://www.mtggoldfish.com/metagame/"
    url_end = "/full#paper" if full is True else "/#paper"
    # weird bug on Pauper requiring lower case. Browsers not affected, but requests is.
    return url_start + formato.lower() + url_end


def fetch_links(formato: str, session: requests.Session, full: bool = True) -> dict[str, str]:
    url = build_url(formato, full)
    print(f"Getting links from {url}")
    page = session.get(url)
    links = grab_links(page.text)
    num_links = len(links)
    print(f"{num_links} links grabbed!!\n")
    return links


def scrape_formato(formato: str,
                   full: bool = True,
                   session: Optional[requests.Session] = None,
                   limit: Optional[int] = None,
                   already_scraped: Optional[Iterable] = None) -> (Dict[str, int], Dict[str, int]):
    """
    Get dict of mains and dict of sides. 
    :formato: str (e.g.: "standard" or "modern")
    :full: bool, True for scraping all decks from /full#paper,
           False for scraping only first decks from /#paper url)
    :session:
    :already_scraped:
    :return:
    """
    mainboards: Dict[str, int] = dict()
    sideboards: Dict[str, int] = dict()

    if session is None:
        session = requests.Session()
    with session as connection:
        links = fetch_links(formato, connection, full)
        if len(links) == 0 and full:
            links = fetch_links(formato, connection, False)
        if limit is not None:
            links = {k: v for k, v in list(links.items())[:limit]}
        for link_name, link in tqdm(links.items()):
            if already_scraped and link_name in already_scraped:
                continue
            # print(f"Getting data from:\n{link}")

            page = connection.get(link).text
            # from Nov 2020, name from grab_links is more correct than scrape_deck_page,
            # so pass it to function directly
            name, mainb, side = scrape_deck_page(page, link_name)
            if name in mainboards:
                print(f"{name} is a CONFLICTING NAME and will not be saved.")
            elif len(mainb) == 0:
                print(f"{name} has EMPTY MAINBOARD and will not be saved.")
            else:
                mainboards[name] = mainb
                sideboards[name] = side

    return mainboards, sideboards


class MtgGoldfishScraper:
    def __init__(self, fullness=False, session=None):
        self.fullness = fullness
        if session is None:
            self.session = requests.Session()
        else:
            self.session = session

    def scrape_formats(self,
                       formats: Union[list[str], tuple[str], set[str]] = (
                               'Standard', 'Modern', 'Pioneer', 'Pauper', 'Legacy',
                               'Vintage', 'Commander_1v1', 'Commander')
                       ):
        if isinstance(formats, str):  # if formats were a str, function would scrape a url for each letter
            formats = (formats,)
        scraped = dict()
        scraped_sideboards = dict()

        for mtg_format in tqdm(formats):
            mainboards, sideboards = self.scrape_format(mtg_format.lower())
            scraped[mtg_format] = mainboards
            for deck_name, sideboard in sideboards.items():
                if sideboard is not None:
                    scraped_sideboards[deck_name] = sideboard

        return scraped, scraped_sideboards

    def scrape_format(self, mtg_format, fullness=None):
        if fullness is None:
            fullness = self.fullness
        return scrape_formato(mtg_format, fullness)

    def scrape_page(self):
        pass


if __name__ == '__main__':
    example_url = "https://www.mtggoldfish.com/metagame/commander/full#paper"
    response = requests.get(example_url)
    deck_links = grab_links(response.text)
    breakpoint()
    page_html = requests.get(list(deck_links.values())[0]).text
    decklist = scrape_deck_page(page_html)
    print(decklist)
