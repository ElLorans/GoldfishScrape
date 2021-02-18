from bs4 import BeautifulSoup


standard_url = 'https://mtgazone.com/metagame/standard'
historic_url = 'https://mtgazone.com/metagame/historic'
historic_brawl_url = 'https://mtgazone.com/decks/historic-brawl/'


def scrape_november_tiers_table(tabula):
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
        for i, stringa in enumerate(records[1]):   # first is empty
            if 'https' in stringa:
                link_index = i
                break

        # Third or Fourth elem is name, Fourt or Fifth is links.
        links = dict()
        try:
            for deck_info in records[1:]:                   # first is empty
                deck_name = deck_info[link_index - 2].split("{")[0]
                deck_link = deck_info[link_index]
                links[deck_name] = deck_link
        except UnboundLocalError:   # Standard has a new UI with 2 tables for BO1 and BO3
            for tab in soup.find_all('table'):
                links.update(scrape_november_tiers_table(tab))

    else:  # for Historic Brawl
        decks = soup.find_all('a', {"class": "_self cvplbd"})
        links = {deck.text.replace(':', '').split(' Historic Brawl Deck')[0]: deck['href'] for deck in decks}
    return links


def get_main_or_side(main_or_side_soup):
    deck = dict()
    for el in main_or_side_soup.find_all('span', {'class': "wp-streamdecker-tooltip"}):
        copies = int(el.find('div', {'class': "card-qty"}).text)
        name = el.find('div', {'class': "card-name"}).text
        name = name.replace('/', ' // ')
        deck[name.split('[')[0].split('<')[0].strip()] = copies
    return deck


def get_mtgazone_deck(mtgazone_deck_html) -> tuple:
    soup = BeautifulSoup(mtgazone_deck_html, 'lxml')
    main = soup.find('div', {'class': "streamdecker-main-deck"})
    side = soup.find('div', {'class': "streamdecker-sideboard"})
    if main is None and side is None:
        return None, None
    if side is None:                                    # for decks without sideboard
        return get_main_or_side(main), {}
    return get_main_or_side(main), get_main_or_side(side)


if __name__ == "__main__":
    import requests
    # standard test

    formato_to_url = {'Standard': standard_url, 'Historic': historic_url, 'Historic Brawl': historic_brawl_url}
    for formato, url in formato_to_url.items():
        response = requests.get(url).text
        mtgazone_links = grab_links(response)
        print(mtgazone_links)
        print('MtgaZoneScraper', formato, ': passed')
