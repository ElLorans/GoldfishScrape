"""
Download all Goldfish decks in a dictionary of dict(int).
"""

import requests
from bs4 import BeautifulSoup


def grab_links(goldfish_html: str, clean=True) -> dict:
    """
    Return ORDERED dict of links to scrape; if param clean is True, decks named only after colours combinations are
        not included.
    :param goldfish_html: html page of goldfish metagame page for a specific format (can be full or partial page)
                          e.g.: https://www.mtggoldfish.com/metagame/modern/full#paper
    :param clean: True or anything else: if clean is not True, decks names like R, UW, etc. are not
                  scraped
    :return: dictionary of deck_names with their links {deck_name: deck_relative_link, ...}
    """

    # split at View More to avoid Budget Decks if program is scraping only partial page
    non_budget = goldfish_html.split("View More")[0]
    soup = BeautifulSoup(non_budget, "lxml")

    names = soup.find_all("span", {"class": "title"})
    name_links = dict()

    permutations = ['W', 'U', 'B', 'R', 'G', 'WU', 'WB', 'WR', 'WG', 'UW', 'UB', 'UR', 'UG', 'BW', 'BU', 'BR', 'BG',
                    'RW', 'RU', 'RB', 'RG', 'GW', 'GU', 'GB', 'GR', 'WUB', 'WUR', 'WUG', 'WBU', 'WBR', 'WBG', 'WRU',
                    'WRB', 'WRG', 'WGU', 'WGB', 'WGR', 'UWB', 'UWR', 'UWG', 'UBW', 'UBR', 'UBG', 'URW', 'URB', 'URG',
                    'UGW', 'UGB', 'UGR', 'BWU', 'BWR', 'BWG', 'BUW', 'BUR', 'BUG', 'BRW', 'BRU', 'BRG', 'BGW', 'BGU',
                    'BGR', 'RWU', 'RWB', 'RWG', 'RUW', 'RUB', 'RUG', 'RBW', 'RBU', 'RBG', 'RGW', 'RGU', 'RGB', 'GWU',
                    'GWB', 'GWR', 'GUW', 'GUB', 'GUR', 'GBW', 'GBU', 'GBR', 'GRW', 'GRU', 'GRB', 'WUBR', 'WUBG', 'WURB',
                    'WURG', 'WUGB', 'WUGR', 'WBUR', 'WBUG', 'WBRU', 'WBRG', 'WBGU', 'WBGR', 'WRUB', 'WRUG', 'WRBU',
                    'WRBG', 'WRGU', 'WRGB', 'WGUB', 'WGUR', 'WGBU', 'WGBR', 'WGRU', 'WGRB', 'UWBR', 'UWBG', 'UWRB',
                    'UWRG', 'UWGB', 'UWGR', 'UBWR', 'UBWG', 'UBRW', 'UBRG', 'UBGW', 'UBGR', 'URWB', 'URWG', 'URBW',
                    'URBG', 'URGW', 'URGB', 'UGWB', 'UGWR', 'UGBW', 'UGBR', 'UGRW', 'UGRB', 'BWUR', 'BWUG', 'BWRU',
                    'BWRG', 'BWGU', 'BWGR', 'BUWR', 'BUWG', 'BURW', 'BURG', 'BUGW', 'BUGR', 'BRWU', 'BRWG', 'BRUW',
                    'BRUG', 'BRGW', 'BRGU', 'BGWU', 'BGWR', 'BGUW', 'BGUR', 'BGRW', 'BGRU', 'RWUB', 'RWUG', 'RWBU',
                    'RWBG', 'RWGU', 'RWGB', 'RUWB', 'RUWG', 'RUBW', 'RUBG', 'RUGW', 'RUGB', 'RBWU', 'RBWG', 'RBUW',
                    'RBUG', 'RBGW', 'RBGU', 'RGWU', 'RGWB', 'RGUW', 'RGUB', 'RGBW', 'RGBU', 'GWUB', 'GWUR', 'GWBU',
                    'GWBR', 'GWRU', 'GWRB', 'GUWB', 'GUWR', 'GUBW', 'GUBR', 'GURW', 'GURB', 'GBWU', 'GBWR', 'GBUW',
                    'GBUR', 'GBRW', 'GBRU', 'GRWU', 'GRWB', 'GRUW', 'GRUB', 'GRBW', 'GRBU', 'WUBRG', 'WUBGR', 'WURBG',
                    'WURGB', 'WUGBR', 'WUGRB', 'WBURG', 'WBUGR', 'WBRUG', 'WBRGU', 'WBGUR', 'WBGRU', 'WRUBG', 'WRUGB',
                    'WRBUG', 'WRBGU', 'WRGUB', 'WRGBU', 'WGUBR', 'WGURB', 'WGBUR', 'WGBRU', 'WGRUB', 'WGRBU', 'UWBRG',
                    'UWBGR', 'UWRBG', 'UWRGB', 'UWGBR', 'UWGRB', 'UBWRG', 'UBWGR', 'UBRWG', 'UBRGW', 'UBGWR', 'UBGRW',
                    'URWBG', 'URWGB', 'URBWG', 'URBGW', 'URGWB', 'URGBW', 'UGWBR', 'UGWRB', 'UGBWR', 'UGBRW', 'UGRWB',
                    'UGRBW', 'BWURG', 'BWUGR', 'BWRUG', 'BWRGU', 'BWGUR', 'BWGRU', 'BUWRG', 'BUWGR', 'BURWG', 'BURGW',
                    'BUGWR', 'BUGRW', 'BRWUG', 'BRWGU', 'BRUWG', 'BRUGW', 'BRGWU', 'BRGUW', 'BGWUR', 'BGWRU', 'BGUWR',
                    'BGURW', 'BGRWU', 'BGRUW', 'RWUBG', 'RWUGB', 'RWBUG', 'RWBGU', 'RWGUB', 'RWGBU', 'RUWBG', 'RUWGB',
                    'RUBWG', 'RUBGW', 'RUGWB', 'RUGBW', 'RBWUG', 'RBWGU', 'RBUWG', 'RBUGW', 'RBGWU', 'RBGUW', 'RGWUB',
                    'RGWBU', 'RGUWB', 'RGUBW', 'RGBWU', 'RGBUW', 'GWUBR', 'GWURB', 'GWBUR', 'GWBRU', 'GWRUB', 'GWRBU',
                    'GUWBR', 'GUWRB', 'GUBWR', 'GUBRW', 'GURWB', 'GURBW', 'GBWUR', 'GBWRU', 'GBUWR', 'GBURW', 'GBRWU',
                    'GBRUW', 'GRWUB', 'GRWBU', 'GRUWB', 'GRUBW', 'GRBWU', 'GRBUW']

    for elem in names:
        name = elem.text.split("\n")[2]

        if name not in name_links and name != 'Other':
            # if deck name already present do NOT insert it in result dict
            if clean is True and name not in permutations:  # exclude decks with bad names
                name_links[name] = "https://www.mtggoldfish.com" + elem.a["href"] + "#paper"

            elif clean is not True:
                name_links[name] = "https://www.mtggoldfish.com" + elem.a["href"] + "#paper"
    return name_links


def scrape_deck_page(html_deck: str) -> (str, dict, dict):
    """
    Get Tuple with Deck Name, Mainboard dict and Sideboard dict from html of deck page.

    :param: html_deck: html page of deck e.g.: https://www.mtggoldfish.com/archetype/standard-jeskai-fires#paper
    :return: tuple (deck_name: str, mainboard: dict, sideboard: dict)
    """
    splitted = html_deck.split("Sideboard")
    mainboard = splitted[0]
    try:
        sideboard = splitted[1].split("Cards Total")[0]
    except IndexError:  # if sideboard does not exist
        sideboard = None

    main_soup = BeautifulSoup(mainboard, "lxml")
    deck_name = main_soup.find("h1", {"class": "deck-view-title"}
                               ).text.strip().replace("\n\nSuggest\xa0a\xa0Better"
                                                      "\xa0Name", "").replace("\nFix Archetype", "")
    if "[" in deck_name:
        deck_name = deck_name[:deck_name.find("[") - 1]

    if "<" in deck_name:
        deck_name = deck_name[:deck_name.find("<") - 1]

    deck_name = deck_name.replace("/", "").replace("-", " ")

    if sideboard is None:
        return deck_name, scrape_cards(main_soup), {}

    side_soup = BeautifulSoup(sideboard, "lxml")
    return deck_name, scrape_cards(main_soup), scrape_cards(side_soup)


def scrape_cards(soup) -> dict:
    """
    Scrape cards in deck list page.
    :param soup: BeautifulSoup of html deck page OF ONLY EITHER mainboard or sideboard
    :type soup: bs4.BeautifulSoup
    :return: dictionary of deck cards {"Mox Opal": 4, ...}
    """
    cells = soup.find_all("td")

    cards = BeautifulSoup(str(cells), "lxml").find_all("td", {"class": "deck-col-card"})
    quantities = BeautifulSoup(str(cells), "lxml").find_all("td", {"class": "deck-col-qty"})

    deck_list = {}
    for index, card in enumerate(cards):
        deck_list[card.text.strip()] = int(quantities[index].text.strip())
    return deck_list


def main(formato, full=False):
    """
    Get dict of mains and dict of sides. 
    :formato: str (e.g.: "standard" or "modern")
    :full: bool (True for scraping all decks from /full#paper and False for scraping only first decks from /#paper url)
    :return:
    """

    url_start = "https://www.mtggoldfish.com/metagame/"
    if full is True:
        url_end = "/full#paper"
    else:
        url_end = "/#paper"
    mainboards = dict()
    sideboards = dict()

    url = url_start + formato + url_end
    print(f"Getting links from {url}")
    page = requests.get(url)
    links = grab_links(page.text).values()

    print(f"{len(links)} links grabbed!!\n")

    for link in links:
        print(f"Getting data from:\n{link}")
        try:
            page = requests.get(link).text
            name, mainb, side = scrape_deck_page(page)
            if name in mainboards:
                print(f"{name} is a CONFLICTING NAME and will not be saved.")
            elif len(mainb) == 0:
                print(f"{name} has EMPTY MAINBOARD and will not be saved.")
            else:
                mainboards[name] = mainb
                sideboards[name] = side
        except TimeoutError:
            print("The connection FAILED due to a TimeOut Error.")
        except Exception as e:
            print(e, "\n", link, "will not be scraped")
    return mainboards, sideboards
