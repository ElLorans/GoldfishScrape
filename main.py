from __future__ import annotations

import logging

import requests
from tqdm.auto import tqdm

from MtgScraper import AetherhubScraper, MtgGoldfishScraper, MtgaZoneScraper, MtgScraper, MtgBoard, clean_database
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


str_to_scraper: dict[str, type[MtgGoldfishScraper] | type[AetherhubScraper] | type[MtgaZoneScraper]] = {
    'MtgGoldfish': MtgGoldfishScraper, 'MtgaZone': MtgaZoneScraper, 'Aetherhub': AetherhubScraper}

if __name__ == "__main__":
    SESSION = requests.Session()
    result = ""
    for formato, sources in tqdm(formats_source.items()):
        clean_formato = formato.replace(" ", "_")
        logging.info(f"\nSwitching to {formato}\n")
        mains: dict[str, MtgBoard] = dict()
        sides: dict[str, MtgBoard] = dict()
        for source in sources:
            try:
                scraper: MtgScraper = str_to_scraper[source](SESSION, clean=True, fullness=False)
                decks = scraper.scrape_format(formato.lower())
            except Exception as e:
                logger.error(f"Error in {source} for {formato}: {e}")
                decks = {}
            for deck_name, deck in decks.items():
                if deck_name not in mains:
                    mains[deck_name] = deck.mainboard
                    if deck.sideboard:
                        sides[deck_name] = deck.sideboard
        result += f"{clean_formato} = {mains} \n{'#' * 80} \n#{clean_formato}_Sideboards \n{clean_formato}_Sideboards = {sides} \n "
        result += f"\n{'#' * 80}\n"
    result = clean_database(result)  # correct misspelled cards
    with open("new_data.py", "w", encoding='utf-8') as f:
        f.write(result)
    logger.info(f"Data saved on new_data.py")
