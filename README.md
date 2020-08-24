# GoldfishScrape
The dataset is used on https://bestdeckforyou.pythonanywhere.com/ (source code at https://github.com/ElLorans/Best-MTG-Deck) to allow users to understand how much they must spend to build each and every tier deck given the cards already in their collection.

Execute 'main.py' to download MtgGoldfish, AetherHub and MtgaZone Decklists as python dictionaries.
All formats in "Standard | Modern | Pioneer | Pauper | Legacy | Vintage | Commander_1v1 | Commander | Brawl | Historic" are scraped.
Run 'main.py' and the output will be saved on 'new_data.py' in the folloqing format:

Standard = {"Deck 1": {"Card 1": 4, ...}, ...} <br>
Standard_Sideboards = {"Deck 1": {"Card 1": 2, ...}, ...} <br>
<br>
Modern = ...<br>
...

---------------------------------------------------------------------------------------------------------------------------------
By default, the program does not scrape decks named "WRGB" or similarly. This behaviour can be changed by modifying the
code from:

links = grab_links(page.text).values() 
to:

links = grab_links(page.text, clean=False).values()

---------------------------------------------------------------------------------------------------------------------------------
MtgScraper contains 3 files with many useful functions in order to scrape single pages, formats and decks from GoldFish, AetherHub and MtgaZone. Import the functions from another .py file for scraping.
