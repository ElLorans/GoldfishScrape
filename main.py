import requests
from bs4 import BeautifulSoup

from MtgScraper import AetherhubScraper, GoldfishScraper, MtgaZoneScraper


if __name__ == "__main__":
    response = requests.get(MtgaZoneScraper.standard_url).text
    mtgazone_standard_links = MtgaZoneScraper.grab_links(response)

    response = requests.get(MtgaZoneScraper.historic_url).text
    mtgazone_historic_links = MtgaZoneScraper.grab_links(response)
    
    fullness = True
    formats = ['Standard', 'Modern', 'Pioneer', 'Pauper', 'Legacy', 'Vintage', 'Commander_1v1', 'Commander']
    print("WATCH OUT: decks with names such as WR and WRBG will not be scraped")
    result = ""
    for formato in formats:
        print("\nSwitching to", formato)
        m, s = GoldfishScraper.main(formato.lower(), fullness)  # main returns 2 variables

        # update with MtgaZone decks
        if formato == 'Standard':
            for name, link in mtgazone_standard_links.items():
                if name not in m:
                    print(f"Adding {name} from MtgaZone at:\n{link}")
                    r = requests.get(link).text
                    try:
                        real_link = BeautifulSoup(r, 'lxml').find('a', {'class': "_self cvplbd"})['href']
                        print(f"Getting data from:\n{real_link}")
                        r = requests.get(real_link).text
                    except TypeError:  # link was already real link
                        pass
                    mtga_m, mtga_s = MtgaZoneScraper.get_mtgazone_deck(r)
                    if mtga_m is not None:
                        m[name] = mtga_m
                        s[name] = mtga_s
                    else:
                        print('No deck found at', link)

        result += f"{formato} = {m} \n{'#' * 80} \n#{formato}_Sideboards \n{formato}_Sideboards = {s} \n "
        result += f"\n{'#' * 80}\n"

    print("Switching to Historic from MtgaZone")
    formato = "Historic"
    m = dict()
    s = dict()
    for name, link in mtgazone_historic_links.items():
        try:
            r = requests.get(link).text
            print(f"Adding {name} from MtgaZone")
            try:
                real_link = BeautifulSoup(r, 'lxml').find('a', {'class': "_self cvplbd"})['href']
                print(f"Getting data from:\n{real_link}")
                r = requests.get(real_link).text
            except TypeError:  # link was already real link
                pass
            mtga_m, mtga_s = MtgaZoneScraper.get_mtgazone_deck(r)
            m[name] = mtga_m
            s[name] = mtga_s
        except Exception as e:
            print(e)
            import pdb; pdb.set_trace()

    result += f"{formato} = {m} \n{'#' * 80} \n#{formato}_Sideboards \n{formato}_Sideboards = {s} \n "
    result += f"\n{'#' * 80}\n"

    print("Switching to Brawl from Aetherhub")
    formato = "Brawl"
    m = AetherhubScraper.main()
    result += f"{formato} = {m} \n{'#' * 80} \n"
    result += f"\n{'#' * 80}\n"

    replacements = {"Dream Den": "Dream-Den", "Lim-Dul": "Lim-Dûl",  # Dream-Den and Lim-Dûl are misspelled on Goldfish
                    # Change Godzilla names
                    "Dorat, the Perfect Pet": "Sprite Dragon", "Mothra, Supersonic Queen": "Luminous Broodmoth",
                    'Gigan, Cyberclaw Terror': 'Gyruda, Doom of Depths',
                    'Babygodzilla, Ruin Reborn': 'Pollywog Symbiote', 'Anguirus, Armored Killer': 'Gemrazer',
                    'Bio-Quartz Spacegodzilla': 'Brokkos, Apex of Forever',
                    ' <292 C>': '', ' [RNA]': '', ' [mps]': '', '\n\nReport Deck Name': '', ' [GRN]': '',          # Goldfish mistakes
                    '\n\nReport Deck Name': ''
                    }

    for k, v in replacements.items():
        result = result.replace(k, v)

    with open("new_data.py", "w", encoding='windows-1252') as f:
        f.write(result)
    print("Data saved on new_data.py")
