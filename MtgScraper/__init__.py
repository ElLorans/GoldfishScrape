from MtgScraper.Aetherhub import AetherhubScraper
from MtgScraper.MtgGoldfish import MtgGoldfishScraper
from MtgScraper.MtgaZone import MtgaZoneScraper
from MtgScraper.base import MtgScraper, MtgSources, FormatName, FormatNameLower
from MtgScraper.mtg_utils import clean_database, MtgBoard, MtgDeck

scrapers: tuple[type[MtgScraper], ...] = (AetherhubScraper, MtgGoldfishScraper, MtgaZoneScraper)
