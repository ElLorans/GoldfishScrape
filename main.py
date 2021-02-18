import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

from MtgScraper import AetherhubScraper, GoldfishScraper, MtgaZoneScraper

if __name__ == "__main__":
    VERBOSE = False
    FULLNESS = True

    verbose_print = print if VERBOSE else lambda *a, **k: None

    print("WATCH OUT: decks with names such as WR and WRBG will not be scraped")
    formats = ('Standard', 'Modern', 'Pioneer', 'Pauper', 'Legacy', 'Vintage', 'Commander_1v1', 'Commander')
    result = ""

    response = requests.get(MtgaZoneScraper.standard_url).text
    mtgazone_standard_links = MtgaZoneScraper.grab_links(response)

    response = requests.get(MtgaZoneScraper.historic_url).text
    mtgazone_historic_links = MtgaZoneScraper.grab_links(response)

    response = requests.get(MtgaZoneScraper.historic_brawl_url).text
    mtgazone_historic_brawl_links = MtgaZoneScraper.grab_links(response)

    for formato in tqdm(formats):
        print("\nSwitching to", formato, "\n")
        m, s = GoldfishScraper.main(formato.lower(), FULLNESS)  # main returns 2 variables

        # update with MtgaZone decks
        if formato == 'Standard':
            for name, link in tqdm(mtgazone_standard_links.items()):
                if name not in m:
                    verbose_print(f"Adding {name} from MtgaZone at:\n{link}")
                    r = requests.get(link).text

                    # r might be landing page of deck archetype (with many similar decks) or real deck
                    try:
                        # get first deck from list of decks inside archetype
                        real_link = BeautifulSoup(r, 'lxml').find('a', {'class': "_self cvplbd"})['href']
                        print(f"Getting data from:\n{real_link}")
                        r = requests.get(real_link).text
                    except TypeError:  # link was already single deck
                        pass

                    mtga_m, mtga_s = MtgaZoneScraper.get_mtgazone_deck(r)
                    if mtga_m is not None:
                        m[name] = mtga_m
                        s[name] = mtga_s
                    else:
                        print('\nNO DECK FOUND AT', link, '\n')

        result += f"{formato} = {m} \n{'#' * 80} \n#{formato}_Sideboards \n{formato}_Sideboards = {s} \n "
        result += f"\n{'#' * 80}\n"

    for formato, links in {'Historic': mtgazone_historic_links,
                           'Historic_Brawl': mtgazone_historic_brawl_links}.items():
        print("Switching to", formato, "from MtgaZone")
        m = dict()
        s = dict()
        for name, link in links.items():
            try:
                r = requests.get(link).text
                verbose_print(f"Adding {name} from MtgaZone at:\n{link}")
                try:
                    real_link = BeautifulSoup(r, 'lxml').find('a', {'class': "_self cvplbd"})['href']
                    verbose_print(f"Getting data from:\n{real_link}")
                    r = requests.get(real_link).text
                except TypeError:  # link was already real link
                    pass
                mtga_m, mtga_s = MtgaZoneScraper.get_mtgazone_deck(r)
                m[name] = mtga_m
                s[name] = mtga_s
            except Exception as e:
                print(e)
                import pdb;

                pdb.set_trace()
        result += f"{formato} = {m} \n{'#' * 80} \n#{formato}_Sideboards \n{formato}_Sideboards = {s} \n "
        result += f"\n{'#' * 80}\n"

    print("Switching to Brawl from Aetherhub")
    formato = "Brawl"
    m = AetherhubScraper.main()
    result += f"{formato} = {m} \n{'#' * 80} \n"
    result += f"\n{'#' * 80}\n"

    replacements = {
        # Dream-Den and Lim-Dûl are misspelled on Goldfish
        "Dream Den": "Dream-Den", "Lim-Dul": "Lim-Dûl",

        # Change Godzilla names
        "Dorat, the Perfect Pet": "Sprite Dragon", "Mothra, Supersonic Queen": "Luminous Broodmoth",
        'Gigan, Cyberclaw Terror': 'Gyruda, Doom of Depths',
        'Babygodzilla, Ruin Reborn': 'Pollywog Symbiote', 'Anguirus, Armored Killer': 'Gemrazer',
        'Bio-Quartz Spacegodzilla': 'Brokkos, Apex of Forever',
        'Godzilla, Doom Inevitable': 'Yidaro, Wandering Monster',
        'Godzilla, King of the Monsters': 'Zilortha, Strength Incarnate',
        'Godzilla, Primeval Champion': 'Titanoth Rex',

        # correct Goldfish mistakes
        ' <292 C>': '', ' [RNA]': '', ' [mps]': '', '\n\nReport Deck Name': '', ' [GRN]': ''
    }

    for k, v in replacements.items():
        result = result.replace(k, v)

    try:
        with open("new_data.py", "w", encoding='windows-1252') as f:
            f.write(result)
    except UnicodeEncodeError as e:
        print(e)
        print("\nSWITCHING TO UTF-8")
        with open("new_data.py", "w", encoding='utf-8') as f:
            f.write(result)
    print("Data saved on new_data.py")
