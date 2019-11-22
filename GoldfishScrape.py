import re
from bs4 import BeautifulSoup
import requests

def grab_links(goldfish_html):
    """
    Return list of links to scrape.
    """
    non_budget = goldfish_html.split("View More")[0]        # split at View More to avoid Budget Decks
    soup = BeautifulSoup(non_budget, "lxml")    
    deck_links = soup.find_all("a", {"class": "card-image-tile-link-overlay"})
    list_links = ["https://www.mtggoldfish.com" + link["href"] + "#paper" for link in deck_links]
    return list_links


def scrape_deck_page(html_deck):
    """
    Separate deck list page.
    :return: tuple (deck_name, mainboard, sideboard)
    """
    splitted = html_deck.split("Sideboard")

    mainboard = splitted[0]
    try:
        sideboard = splitted[1].split("Cards Total")[0]
    except IndexError:  # if sideboard does not exist
        sideboard = None

    main_soup = BeautifulSoup(mainboard, "lxml")
    deck_name = main_soup.find("h1", {"class": "deck-view-title"}).text.strip().replace("\n\nSuggest\xa0a\xa0Better"
                                                          "\xa0Name", "")
    
    if sideboard is None:
        return deck_name, scrape_cards(main_soup), {"None": 0}

    side_soup = BeautifulSoup(sideboard, "lxml")

    return deck_name, scrape_cards(main_soup), scrape_cards(side_soup)



def scrape_cards(soup):
    """
    Scrape cards in deck list page.
    """
    cells = soup.find_all("td")

    cards = BeautifulSoup(str(cells), "lxml").find_all("td", {"class":
                                                                  "deck-col-card"})
    quantities = BeautifulSoup(str(cells), "lxml").find_all("td", {"class":
                                                                       "deck-col-qty"})

    deck_list = {}
    for index, card in enumerate(cards):
        deck_list[card.text.strip()] = int(quantities[index].text.strip())
    return deck_list


def main(formato, full=False):
    """
    :formato: str (e.g.: "standard" or "modern")
    """
    URL_START = "https://www.mtggoldfish.com/metagame/"
    if full is True:
        URL_END = "/full#paper"
    else:
        URL_END = "/#paper"
    mainboards = dict()
    sideboards = dict()

    url = URL_START + formato + URL_END
    page = requests.get(url)
    
    list_links = grab_links(page.text)
    
    for link in list_links:
        print(link)
        page = requests.get(link).text
        name, main, side = scrape_deck_page(page)
        mainboards[name] = main
        sideboards[name] = side
    return mainboards, sideboards


if __name__ == "__main__":
    target = input("Insert format to scrape").lower()
    fullness = input("Do you want to download all decks (Suggested for Modern and Legacy)?(y/n)").lower()
    if fullness[0] == "y":
        fullness = True
    else:
        fullness = False
    m, s = main(target, fullness)
    confirmation = input("Save results?(y/n)").lower()
    if confirmation[0] == "y":
        import json

        with open(target + "_m.json", "w") as j:
            json.dump(m, j)
        with open(target + "_s.json", "w") as f:
            json.dump(s, f)
        print("Output saved to", target + "_m.json", "and", target + "_s.json")

