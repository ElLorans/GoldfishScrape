The project needs a refactor to use async to speed up scraping
(without scraping 2 urls from the same website, but e.g. scraping at the same time from both Goldfish and AetherHub)

# GoldfishScrape
Execute 'main.py' to download MtgGoldfish, AetherHub and MtgaZone Decklists as python dictionaries.
Edit input_formats.py to choose what formats to scrape from which source.

The dataset is used on https://bestdeckforyou.pythonanywhere.com/ (source code at https://github.com/ElLorans/Best-MTG-Deck) to allow users to understand how much they must spend to build each and every MTG tier deck given the cards already in their collection.

Run 'main.py' and the output will be saved on 'new_data.py' in the following format:

Standard = {"Deck 1": {"Card 1": 4, ...}, ...} <br>
Standard_Sideboards = {"Deck 1": {"Card 1": 2, ...}, ...} <br>
<br>
Modern = ...<br>
...

---------------------------------------------------------------------------------------------------------------------------------
By default, the program does not scrape decks named "WRGB" or similarly. This behaviour can be changed by modifying the
code from: 
<br>

links = grab_links(page.text).values()
<br>
to:

links = grab_links(page.text, clean=False).values()

---------------------------------------------------------------------------------------------------------------------------------
MtgScraper contains many files with useful functions in order to scrape single pages, formats and decks from GoldFish, AetherHub and MtgaZone. Import the functions from another .py file for scraping.
