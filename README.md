# GoldfishScrape
Download MtgGoldfish Decklists as python dictionaries.
All formats in "Standard | Modern | Pioneer | Pauper | Legacy | Vintage | Commander_1v1 | Commander | Brawl | Historic" are scraped.
Run goldfishscrape.py and the output will be saved on "new_data.py" in the folloqing format:

Standard = {"Deck 1": {"Card 1": 4, ...}, ...}
Standard_Sideboards = {"Deck 1": {"Card 1": 2, ...}, ...}
...

---------------------------------------------------------------------------------------------------------------------------------
By default, the program does not scrape decks named "WRGB" or similarly. This behaviour can be changed by modifying the
line 144 from:

links = grab_links(page.text).values() 
to:

links = grab_links(page.text, clean=False).values()

---------------------------------------------------------------------------------------------------------------------------------
goldfishscrape.py contains many useful functions in order to scrape single pages, formats and decks on GoldFish. Import the functions from another .py file for scraping.
