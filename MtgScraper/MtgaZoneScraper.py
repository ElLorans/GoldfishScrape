from typing import Optional, Tuple, Iterable

import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

standard_url = 'https://mtgazone.com/metagame/standard'
historic_url = 'https://mtgazone.com/metagame/historic'
historic_brawl_url = 'https://mtgazone.com/decks/historic-brawl/'


def grab_november_tiers_table(tabula: BeautifulSoup) -> dict:
    """
    Scrape Table after November UI change.
    :return:
    """
    links = dict()
    for tr in tabula.find_all("tr"):
        # ths = tr.find_all("th")
        trs = tr.find_all("td")
        for cell in trs:
            a = cell.find('a')
            name = cell.text
            if a is not None and len(name) > 0:
                link = a['href']
                link = link if link.startswith('https://mtgazone.com') else 'https://mtgazone.com' + link
                links[name] = link
    return links


def grab_links(mtgazone_html: str) -> dict:
    """
    Return dict name: link (standard, historic) of ORDERED links to scrape.
    :param mtgazone_html: html page of mtgazone metagame page for all formats
    :return: dictionary {deck_name: deck_relative_link, ...} of relative format (either standard or historic)
    """
    soup = BeautifulSoup(mtgazone_html, 'lxml')
    table = soup.find('table')
    if table is not None:
        records = list()
        for tr in table.find_all("tr"):
            # ths = tr.find_all("th")
            trs = tr.find_all("td")
            record = list()
            for each in trs:
                if each.text == 'Decks':
                    link = each.find('a')['href']
                    # change relative links to absolute links
                    link = link if link.startswith('https://mtgazone.com') else 'https://mtgazone.com' + link
                    record.append(link)
                record.append(each.text)
            records.append(record)

        # get link position as it changes btw standard and historic
        for i, stringa in enumerate(records[1]):  # first is empty
            if 'https' in stringa:
                link_index = i
                break

        # Third or Fourth elem is name, Fourt or Fifth is links.
        links = dict()
        try:
            for deck_info in records[1:]:  # first is empty
                deck_name = deck_info[link_index - 2].split("{")[0]
                deck_link = deck_info[link_index]
                links[deck_name] = deck_link
        except UnboundLocalError:  # Standard has a new UI with 2 tables for BO1 and BO3
            for tab in soup.find_all('table'):
                links.update(grab_november_tiers_table(tab))

    else:  # for Historic Brawl
        decks = soup.find_all('a', {"class": "_self cvplbd"})
        links = {deck.text.replace(':', '').split(' Historic Brawl Deck')[0]: deck['href'] for deck in decks}
    return links


def get_main_or_side(main_or_side_soup: BeautifulSoup) -> dict[str, int]:
    deck = dict()
    cards = main_or_side_soup.find_all("div", {"class": "card"})
    for card in cards:
        deck[card["data-name"]] = int(card["data-quantity"])
    return deck


def get_mtgazone_deck(mtgazone_deck_html: str) -> Tuple[Optional[dict], Optional[dict]]:
    soup = BeautifulSoup(mtgazone_deck_html, 'lxml')
    main = soup.find("div", {"class": "decklist main"})
    side = soup.find("div", {"class": "decklist sideboard"})
    if main is None and side is None:
        return None, None
    if side is None:  # for decks without sideboard
        return get_main_or_side(main), {}
    return get_main_or_side(main), get_main_or_side(side)


def scrape_mtgazone_deck(link: str, session: Optional[requests.Session] = None) -> \
        Tuple[Optional[dict], Optional[dict]]:
    """
    MtgaZone has landing page for archetype with many decks: this function returns the mtg deck from the first deck in
    the archetype url; if it finds no deck link it returns the deck ftom link.
    :param link:
    :param session: requests.Session(), optional to increase speed
    :return:
    """
    req_session = session if session else requests.Session()

    with req_session as session:
        mtgazone_html = session.get(link).text
        try:
            real_link = BeautifulSoup(mtgazone_html, 'lxml').find('a', {'class': "_self cvplbd"})['href']
            mtgazone_html = session.get(real_link).text
        except TypeError:  # link was already real link
            pass
    mainboard, sideboard = get_mtgazone_deck(mtgazone_html)
    return mainboard, sideboard


def scrape_formato(format_name: str, session: Optional[requests.Session] = None, limit: Optional[int] = None,
                   already_scraped: Optional[Iterable] = None) -> (
        dict[str, int], dict[str, int]):
    """

    :param already_scraped:
    :param format_name:
    :param session:
    :param limit: Optional[int] to limit number of results (useful in testing)
    :return:
    """
    formato_to_url = {'standard': standard_url, 'historic': historic_url, 'historic_brawl': historic_brawl_url}
    if format_name not in formato_to_url:
        print(format_name, "not implemented on MtgaZone")
        return {}, {}
    session = requests.Session() if session is None else session

    result = dict()
    result_sideboard = dict()
    with session as session:
        links = grab_links(session.get(formato_to_url[format_name]).text)
        if limit is not None:
            links = {k: v for k, v in list(links.items())[:limit]}
        for deck_name, link in tqdm(links.items()):
            if already_scraped and deck_name in already_scraped:
                continue
            mtga_m, mtga_s = scrape_mtgazone_deck(link, session)
            result[deck_name] = mtga_m
            result_sideboard[deck_name] = mtga_s
    return result, result_sideboard


if __name__ == "__main__":
    test_session = requests.session()
    mains, sides = scrape_formato("Standard",
                                  session=test_session,
                                  limit=1)
    breakpoint()
