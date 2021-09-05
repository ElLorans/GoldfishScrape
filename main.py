"""
Scrape from MtgGoldfish: Standard', 'Modern', 'Pioneer', 'Pauper', 'Legacy', 'Vintage', 'Commander_1v1', 'Commander'
Scrape missing decks for ('Standard', 'Historic') from MtgaZone
Scrape 'Historic Brawl' from MtgaZone
Scrape 'Brawl' from AetherHub
"""

import logging

import requests
from tqdm.auto import tqdm

from MtgScraper import clean_database, AetherhubScraper, GoldfishScraper, MtgaZoneScraper


def write_db(data: str, file_name):
    try:
        with open(file_name, "a", encoding='windows-1252') as f:
            f.write(data)
    except UnicodeEncodeError as e:
        logger.exception(e)
        logger.warning("\nSWITCHING TO UTF-8")
        with open(file_name, "a", encoding='utf-8') as f:
            f.write(data)
    logger.info(f"Data saved on {file_name}")


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

# Brawl is from AetherHub
# Standard is combined with data from MtgaZone
# Historic and Historic_Brawl are from MtgaZone
FORMATS = ('Standard', 'Historic', 'Historic Brawl', 'Pioneer', 'Modern', 'Legacy', 'Vintage',
           'Pauper', 'Commander', 'Commander_1v1')
FORMATS = ('Historic Brawl', )

MTGAZONE_URLS = {"MtgaZone_Standard": MtgaZoneScraper.standard_url,
                 "MtgaZone_Historic": MtgaZoneScraper.historic_url,
                 "MtgaZone_HistoricBrawl": MtgaZoneScraper.historic_brawl_url
                 }

session = requests.Session()
MTGAZONE_LINKS = dict()
for links_name, url in MTGAZONE_URLS.items():
    MTGAZONE_LINKS[links_name] = MtgaZoneScraper.grab_links(session.get(url).text)

HISTORIC_LINKS = {'Historic': MTGAZONE_LINKS['MtgaZone_Historic'],
                  'Historic Brawl': MTGAZONE_LINKS['MtgaZone_HistoricBrawl']}


if __name__ == "__main__":
    result = ""

    for formato in tqdm(FORMATS):
        logger.info("\nSwitching to", formato, "\n")
        m, s = GoldfishScraper.main(formato.lower())  # main returns 2 variables
        # update with MtgaZone decks
        if formato == 'Standard':
            for name, link in tqdm(MTGAZONE_LINKS['MtgaZone_Standard'].items()):
                if name not in m:
                    # FALSE is for sorting log file
                    logger.debug(f"Scraping {name} from MtgaZone at:\n{link}")
                    mtga_m, mtga_s = MtgaZoneScraper.scrape_mtgazone_deck(link)
                    if mtga_m is not None:
                        m[name] = mtga_m
                        s[name] = mtga_s
                    else:
                        logger.debug(f'NO DECK FOUND AT {link}')

        elif formato in HISTORIC_LINKS:
            logger.info(f"Switching to {formato} from MtgaZone")
            m = dict()
            s = dict()
            # for name, link in tqdm(historic_formats_links[formato].items()):
            breakpoint()
            for name, link in tqdm(HISTORIC_LINKS[formato].items()):
                mtgazone_html = session.get(link).text
                logger.debug(f"Adding {name} from MtgaZone at:\n{link}")
                mtga_m, mtga_s = MtgaZoneScraper.scrape_mtgazone_deck(link)
                if mtga_m is not None:
                    m[name] = mtga_m
                    s[name] = mtga_s
                else:
                    logger.debug(f'NO DECK FOUND AT {link}')
            clean_formato = formato.replace(" ", "_")
            result += f"{clean_formato} = {m} \n{'#' * 80} \n#{clean_formato}_Sideboards \n{clean_formato}_Sideboards = {s} \n "
            result += f"\n{'#' * 80}\n"
        clean_formato = formato.replace(" ", "_")
        result += f"{clean_formato} = {m} \n{'#' * 80} \n#{clean_formato}_Sideboards \n{clean_formato}_Sideboards = {s} \n "
        result += f"\n{'#' * 80}\n"

    logger.info("Switching to Brawl from Aetherhub")
    formato = "Brawl"
    m = AetherhubScraper.main()
    result += f"{formato} = {m} \n{'#' * 80} \n"
    result += f"\n{'#' * 80}\n"

    result = clean_database(result)  # correct misspelled cards

    session.close()
    write_db(result, "new_data.py")
