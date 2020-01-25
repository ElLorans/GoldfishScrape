# GoldfishScrape
Download MtgGoldfish Decklists as python dictionaries.

Run goldfishscrape.py. Insert the format you want to scrape (e.g.: Modern). The screen will show all the urls being scraped.
The script will ask if you want to save the output. If "yes" is inserted, you will get "modern.py" including a dictionary 
named Modern and another one named Modern_Sideboards.

By default, the program does not scraped decks named "WRGB" or similarly. This behaviour can be changed by modifying the
line 144 from:

links = grab_links(page.text).values() 
to:

links = grab_links(page.text, clean=False).values()
