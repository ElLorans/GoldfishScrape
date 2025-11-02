"""Scrape each format_source key from the sources specified in the Iterable value.
The order in the Iterable gives priority: Decks with the same name will be scraped by the second source, but not saved.
"""
from __future__ import annotations
from typing import Iterable

from MtgScraper import FormatName, MtgSources

formats_source: dict[FormatName, Iterable[MtgSources]] = {
    'Standard': ('MtgGoldfish', 'MtgaZone',),
    'Alchemy': ('MtgGoldfish',),
    'Timeless': ('MtgaZone',),
    'Historic': ('MtgaZone',),
    'Brawl': ('MtgGoldfish', ),
    # 'Historic Brawl': ('Aetherhub', ),
    'Pioneer': ('MtgGoldfish',),
    'Modern': ('MtgGoldfish',),
    'Legacy': ('MtgGoldfish',),
    'Vintage': ('MtgGoldfish',),
    'Pauper': ('MtgGoldfish',),
    'Commander': ('MtgGoldfish',),
    'Duel Commander': ('MtgGoldfish',)
}
