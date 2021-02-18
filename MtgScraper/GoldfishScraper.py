"""
Download all Goldfish decks in a dictionary.
"""
from bs4 import BeautifulSoup
import requests


def deck_text_to_dict(stringa: str) -> dict:
    """
    Convert plain text to dictionary. Text must be separated by \n and number of copies must be separated by ' ' from
    card names.
    :param stringa: '1 Card\n3 OtherCard\n...'
    :return: {'Card': 1, 'OtherCard': 3...}
    """
    decklist = dict()
    for el in stringa.split('\n'):
        if len(el.strip()) > 0:
            copies, card = el.split(' ', 1)
            decklist[card.split('[')[0].split('<')[0].strip()] = int(copies)
    return decklist


def grab_links(gf_html: str, clean=True) -> dict:
    """
    Return ORDERED dict of links to scrape; if param clean is True, decks named only after colours combinations are
        not included.
    :param gf_html: html page of goldfish metagame page for a specific format (can be full or partial page)
                          e.g.: https://www.mtggoldfish.com/metagame/modern/full#paper
    :param clean: True or anything else: if clean is not True, decks names like R, UW, etc. are not
                  scraped
    :return: dictionary of deck_names with their links {deck_name: deck_relative_link, ...}
    """
    # split at View More to avoid Budget Decks if program is scraping only partial page
    non_budget = gf_html.split("View More")[0]
    soup = BeautifulSoup(non_budget, "lxml")

    names = soup.find_all('span', {'class': 'deck-price-paper'})[1:]
    name_links = dict()
    permutations = {'W', 'U', 'B', 'R', 'G', 'WU', 'WB', 'WR', 'WG', 'UW', 'UB', 'UR', 'UG', 'BW', 'BU', 'BR', 'BG',
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
                    'GBRUW', 'GRWUB', 'GRWBU', 'GRUWB', 'GRUBW', 'GRBWU', 'GRBUW'}

    for elem in names:
        name = elem.text.replace('\n', '')

        if name not in name_links and name != 'Other':
            # if deck name already present do NOT insert it in result dict
            if clean is True and name not in permutations:  # exclude decks with bad names
                name_links[name] = "https://www.mtggoldfish.com" + elem.a["href"]

            elif clean is not True:
                name_links[name] = "https://www.mtggoldfish.com" + elem.a["href"]
    return name_links


def scrape_deck_page(html_deck: str) -> (str, dict, dict):
    """
    Get Tuple with Deck Name, Mainboard dict and Sideboard dict from html of deck page.

    :param: html_deck: html page of deck e.g.: https://www.mtggoldfish.com/archetype/standard-jeskai-fires#paper
    :return: tuple (deck_name: str, mainboard: dict, sideboard: dict)
    """
    soup = BeautifulSoup(html_deck, "lxml")

    # find author, then get parent node. Easiest way I could find to exclude author from deck name.
    # Structure:
    # <h1 class ="title">
    #   Four - Color Omnath
    #   <span class ="author"> by VTCLA </span>
    # </h1>
    deck_name = soup.find("span", {"class": "author"}).previousSibling.replace('\n', '').strip()
    deck_name = deck_name.replace("/", "").replace("-", " ").replace("\n\nSuggest\xa0a\xa0Better\xa0Name", "").replace(
        "\nFix Archetype", "")

    if "[" in deck_name:
        deck_name = deck_name[:deck_name.find("[") - 1]

    if "<" in deck_name:
        deck_name = deck_name[:deck_name.find("<") - 1]
    if "{" in deck_name:
        breakpoint()

    main, side = scrape_cards(soup)
    return deck_name, main, side


def scrape_cards(html_soup: BeautifulSoup) -> tuple:
    """
    Scrape cards in deck list page.
    :param html_soup: BeautifulSoup of html deck page OF both mainboard or sideboard
    :return: tuple of dictionaries of deck cards ({"Mox Opal": 4, ...}, {"Galvanic Blast": 2, ...})
    """
    deck_plain_text = html_soup.find('input', {'id': "deck_input_deck"})['value']
    main_text, side_text = deck_plain_text.split('sideboard')

    return deck_text_to_dict(main_text), deck_text_to_dict(side_text)


def main(formato, full=False):
    """
    Get dict of mains and dict of sides. 
    :formato: str (e.g.: "standard" or "modern")
    :full: bool, True for scraping all decks from /full#paper,
           False for scraping only first decks from /#paper url)
    :return:
    """
    url_start = "https://www.mtggoldfish.com/metagame/"
    url_end = "/full#paper" if full is True else "/#paper"

    mainboards = dict()
    sideboards = dict()

    url = url_start + formato + url_end
    print(f"Getting links from {url}")
    page = requests.get(url)
    links = grab_links(page.text)   #.values()

    print(f"{len(links)} links grabbed!!\n")

    for link_name, link in links.items():
        print(f"Getting data from:\n{link}")
        try:
            page = requests.get(link).text
            name, mainb, side = scrape_deck_page(page)
            # from Nov 2020, name from grab_links is more correct than scrape_deck_page
            name = link_name
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


if __name__ == '__main__':
    url = "https://www.mtggoldfish.com/metagame/standard/full#paper"
    page = requests.get(url)
    links = grab_links(page.text)

    import pdb; pdb.set_trace()
    page_html = requests.get(list(links.values())[0]).text
    decklist = scrape_deck_page(page_html)
    print(decklist)
