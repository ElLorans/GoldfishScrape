# Scrape brawl from Aetherhub
from io import StringIO
from typing import Optional, Iterable

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm


def grab_brawl_links(html: str) -> dict[str, str]:
    soup = BeautifulSoup(html, 'lxml')
    brawl_data = soup.find_all('td', {'class': "text-left meta-border-top ae-decktitle"})
    brawl = {el.text.strip(): 'https://aetherhub.com' + el.find('a')['href'] for el in brawl_data}
    return brawl


def scrape_formato(format_name: str, session: Optional[requests.Session] = None, limit: Optional[int] = None,
                   already_scraped: Optional[Iterable] = None) -> tuple[dict[str, int], dict[str, int]]:
    """

    :param already_scraped:
    :param limit:
    :param format_name:
    :param session:
    :return: tuple with first elem mainboards, second elem sideboards (for Brawl default to None)
    """
    if format_name != "brawl":
        print(format_name, "not implemented on AetherHub")
        return {}, {}
    # "brawl" not accepted, only "Brawl"
    url = f'https://aetherhub.com/Meta/Metagame/{format_name.title()}/'
    session = requests.Session() if session is None else session

    with session as connection:
        r = connection.get(url).text
        links = grab_brawl_links(r)
        if limit is not None:
            links = {k: v for k, v in list(links.items())[:limit]}
        deck_lists: dict[str, int] = dict()
        for name, link in tqdm(links.items()):
            if already_scraped and name in already_scraped:
                continue
            r = connection.get(link).text
            dfs = pd.read_html(StringIO(r))  # pd.read_html captures commander as well, bs4 struggles to do so
            # dfs[0] first col is commander
            # dfs[1] first col is decklist
            deck_list = dfs[0][0].to_list() + dfs[1].iloc[:, 0].to_list()

            deck = dict()
            for el in deck_list:
                if '(' not in el:
                    copies, card = el.split(' ', 1)
                    deck[card.split('[')[0].split('<')[0].strip()] = int(copies)
            deck_lists[name] = deck
    return deck_lists, {}


if __name__ == "__main__":
    test_session = requests.session()
    mains, sides = scrape_formato("brawl",
                                  session=test_session,
                                  limit=1)
    print(mains)
