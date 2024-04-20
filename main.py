"""
Scrape from MtgGoldfish: Standard', 'Modern', 'Pioneer', 'Pauper', 'Legacy', 'Vintage', 'Commander_1v1', 'Commander'
Scrape missing decks for ('Standard', 'Historic') from MtgaZone
Scrape 'Historic Brawl' from MtgaZone
Scrape 'Brawl' from AetherHub
"""

from __future__ import annotations

import logging

import requests
from tqdm.auto import tqdm

from MtgScraper import AetherhubScraper, GoldfishScraper, MtgaZoneScraper
from MtgScraper.mtg_utils import clean_database
from input_formats import formats_source

# set logging /
logger = logging.getLogger('MtgScraper')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s,%(name)s,%(message)s')

file_handler = logging.FileHandler('MtgScraperLog.csv', mode='w')
stream_handler = logging.StreamHandler()

for handler in (file_handler, stream_handler):
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
# / set logging


str_to_scraper: dict[str, GoldfishScraper | AetherhubScraper | MtgaZoneScraper] = {
    'MtgGoldfish': GoldfishScraper,
    'MtgaZone': MtgaZoneScraper,
    'Aetherhub': AetherhubScraper
}

if __name__ == "__main__":
    SESSION = requests.Session()
    result = ""
    for formato, sources in tqdm(formats_source.items()):
        clean_formato = formato.replace(" ", "_")
        logging.info(f"\nSwitching to {formato}\n")
        mains = dict()
        sides = dict()
        for source in sources:
            # scrape_formato returns 2 variables
            m, s = str_to_scraper[source].scrape_formato(formato.lower(),
                                                         session=SESSION,
                                                         already_scraped=mains.keys(),
                                                         )
            mains.update(m)
            sides.update(s)
        result += f"{clean_formato} = {mains} \n{'#' * 80} \n#{clean_formato}_Sideboards \n{clean_formato}_Sideboards = {sides} \n "
        result += f"\n{'#' * 80}\n"
    result = clean_database(result)  # correct misspelled cards
    with open("new_data.py", "w", encoding='utf-8') as f:
        f.write(result)
    logger.info(f"Data saved on new_data.py")
