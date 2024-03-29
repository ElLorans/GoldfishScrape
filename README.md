The project needs a major restructuring.
Objective: provide a common, stable API to scrape he most famous MTG websites for deck lists.
First Milestone: refactor code.
Second Milestone: Define a simple API to establish which formats to scrape and priorities (e.g.: if same deck is found on Goldfish and AetherHub, which one is to be scraped?)
Third Milestone: use async to speed up scraping (without scraping 2 urls from the same website, but e.g. scraping at the same time from both Goldfish and AetherHub)

Second Step: use async to speed up scraping. Since
# GoldfishScrape
Execute 'main.py' to download MtgGoldfish, AetherHub and MtgaZone Decklists as python dictionaries.
All formats in 
<br>
"Standard | Modern | Pioneer | Pauper | Legacy | Vintage | Commander_1v1 | Commander | Brawl | Historic"
<br> and Historic Brawl are scraped.
<br>

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
MtgScraper contains 3 files with many useful functions in order to scrape single pages, formats and decks from GoldFish, AetherHub and MtgaZone. Import the functions from another .py file for scraping.
