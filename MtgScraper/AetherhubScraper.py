# Scrape brawl from Aetherhub

from bs4 import BeautifulSoup
import pandas as pd
import requests


def grab_brawl_links(html):
    soup = BeautifulSoup(html, 'lxml')
    brawl_data = soup.find_all('td', {'class': "text-left meta-border-top ae-decktitle"})
    brawl = {el.text.strip(): 'https://aetherhub.com' + el.find('a')['href'] for el in brawl_data}
    return brawl
    

def main():
    url = 'https://aetherhub.com/Meta/Metagame/Brawl/'
    r = requests.get(url).text
    meta = grab_brawl_links(r)
    
    deck_lists = dict()
    for name, link in meta.items():
        r = requests.get(link).text
        dfs = pd.read_html(r)                    # pd.read_html captures commander as well, bs4 struggles to do so
        # dfs[0] first col is commander
        # dfs[1] first col is decklist
        deck_list = dfs[0][0].to_list() + dfs[1].iloc[:, 0].to_list()
        
        deck = dict()
        for el in deck_list:
            if '(' not in el:
                copies, card = el.split(' ', 1)
                deck[card.split('[')[0].split('<')[0].strip()] = int(copies)
        deck_lists[name] = deck
        
    return deck_lists


if __name__ == "__main__":
    formato = "Brawl"
    m = main()
    result = f"{formato} = {m} \n{'#' * 80} \n"
    result += f"\n{'#' * 80}\n"
    file = "brawl.py"
    with open(file, "w", encoding='windows-1252') as f:
        f.write(result)
    print('Data saved to', file)