"""Scrape each format_source key from the sources specified in the Iterable value.
The order in the Iterable gives priority: Decks with the same name will not be scraped from the second source.
"""
from __future__ import annotations
from typing import Iterable


formats_source: dict[str, Iterable[str]] = {
    'Standard': ('MtgGoldfish', 'MtgaZone',),
    'Alchemy': ('MtgGoldfish',),
    'Timeless': ('MtgaZone',),
    'Historic': ('MtgaZone',),
    'Brawl': ('Aetherhub', ),
    'Historic Brawl': ('Aetherhub', ),
    'Pioneer': ('MtgGoldfish',),
    'Modern': ('MtgGoldfish',),
    'Legacy': ('MtgGoldfish',),
    # 'Vintage': ('MtgGoldfish',),
    'Pauper': ('MtgGoldfish',),
    'Historic_Brawl': ('MtgaZone', ),
    'Commander': ('MtgGoldfish',),
    'Commander_1v1': ('MtgGoldfish',)
}
