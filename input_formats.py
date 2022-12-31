"""Scrape from MtgGoldfish: Standard', 'Modern', 'Pioneer', 'Pauper', 'Legacy', 'Vintage', 'Commander_1v1','
Commander'
Scrape missing decks for ('Standard', 'Historic') from MtgaZone
Scrape 'Historic Brawl' from MtgaZone
Scrape 'Brawl' from AetherHub
"""
formats_source: dict[str, tuple] = {
    'Standard': ('MtgGoldfish', 'MtgaZone',),
    'Alchemy': ('MtgGoldfish',),
    'Historic': ('MtgaZone',),
    'Brawl': ('Aetherhub', ),
    'Historic Brawl': ('Aetherhub', ),
    'Pioneer': ('MtgGoldfish',),
    'Modern': ('MtgGoldfish',),
    'Legacy': ('MtgGoldfish',),
    'Vintage': ('MtgGoldfish',),
    'Pauper': ('MtgGoldfish',),
    'Historic_Brawl': ('MtgaZone', ),
    'Commander': ('MtgGoldfish',),
    'Commander_1v1': ('MtgGoldfish',)
}
