"""
class MtgBoard
class MtgDeck
func clean_database
"""


class MtgBoard(dict):
    """
    Acts as a Dict[str, int] that accepts only str as keys and int as values.
    """

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError("Key should be str, not", type(key))
        if not isinstance(value, int):
            raise TypeError("Key should be int, not", type(value))
        super().__setitem__(key, value)

    def __getitem__(self, key):
        super().__getitem__(key)

    def __repr__(self):
        return super().__repr__()


class MtgDeck:
    """
    A class with 2 attributes that act as Dict[str, int]: mainboard and sideboard.
    """

    def __init__(self, mainboard=None, sideboard=None):
        if mainboard is None:
            self.mainboard = MtgBoard()
        else:
            self.mainboard = mainboard

        if sideboard is None:
            self.sideboard = MtgBoard()
        else:
            self.sideboard = sideboard

    def __repr__(self):
        return f"Mainboard: {self.mainboard.__repr__()}\nSideboard: {self.sideboard.__repr__()}"


def deck_text_to_dict(stringa: str) -> MtgBoard:
    """
    Convert plain text to dictionary. Text must be separated by \n and number of copies must be separated by ' ' from
    card names.
    :param stringa: '1 Card\n3 OtherCard\n...'
    :return: {'Card': 1, 'OtherCard': 3...}
    """
    deck_list = MtgBoard()
    for line in stringa.splitlines():
        if len(line.strip()) > 0:
            copies, card = line.split(' ', 1)
            card = card.split('[')[0].split('<')[0].strip()
            deck_list[card] = deck_list.get(card, 0) + int(copies)
    return deck_list


def clean_database(stringa: str) -> str:
    replacements = {
        # Dream-Den and Lim-Dûl are misspelled on Goldfish
        "Dream Den": "Dream-Den", "Lim-Dul": "Lim-Dûl", "Lim-D�l": "Lim-Dûl",

        # Change Godzilla names
        "Dorat, the Perfect Pet": "Sprite Dragon", "Mothra, Supersonic Queen": "Luminous Broodmoth",
        'Gigan, Cyberclaw Terror': 'Gyruda, Doom of Depths',
        'Babygodzilla, Ruin Reborn': 'Pollywog Symbiote', 'Anguirus, Armored Killer': 'Gemrazer',
        'Bio-Quartz Spacegodzilla': 'Brokkos, Apex of Forever',
        'Godzilla, Doom Inevitable': 'Yidaro, Wandering Monster',
        'Godzilla, King of the Monsters': 'Zilortha, Strength Incarnate',
        'Godzilla, Primeval Champion': 'Titanoth Rex',

        # correct Goldfish mistakes
        ' <292 C>': '', ' [RNA]': '', ' [mps]': '', '\n\nReport Deck Name': '', ' [GRN]': '',
        "A - Oran - Rief Ooze": "Oran-Rief Ooze",
        "a-Dragon's Rage Channeler": "Dragon's rage channeler",
        "Sakurtribe Elder": "Sakura-Tribe Elder",

        # Double Face Cards
        'Mistgate Pathway': 'Hengegate Pathway // Mistgate Pathway',
        'Grimclimb Pathway': 'Brightclimb Pathway // Grimclimb Pathway',
        'Agadeem, the Undercrypt': "Agadeem's Awakening // Agadeem, the Undercrypt",
        'Pick-Beeble': 'Pick-a-Beeble',
        'Lagonnband Trailblazer': 'Lagonna-Band Trailblazer',
        'Sedasher Octopus': 'Sea-Dasher Octopus',

        '///': '//',

        # LOTR accents
        "Gloin, Dwarf Emissary": "Glóin, Dwarf Emissary",
        "Smeagol, helpful guide": "Sméagol, helpful guide",
        "Palantir of Orthanc": "Palantír of Orthanc",
        "Lord of the Nazgul": "Lord of the Nazgûl",
        "Troll of Khazad-dum": "Troll of Khazad-dûm",
        "Lorien Revealed": "Lórien Revealed",
        "Anduril, Flame of the West": "Andúril, Flame of the West",
        "Mauhur": "Mauhúr",
        "Barad-dur": "Barad-dûr",
        'Eomer, King of Rohan': 'Éomer, King of Rohan',
        'Eowyn, Shieldmaiden': 'Éowyn, Shieldmaiden',
        'Theoden, King of Rohan': 'Théoden, King of Rohan',
        'Gilraen, Dunedain Protector': 'Gilraen, Dúnedain Protector',
        'Haldir, Lorien Lieutenant': 'Haldir, Lórien Lieutenant',
        'Lothlorien Lookout': 'Lothlórien Lookout',
        'Soothing of Smeagol': 'Soothing of Sméagol',

    }

    for k, v in replacements.items():
        stringa = stringa.replace(k, v)
    return stringa


# names not to be considered
unclear_deck_names = {'W', 'U', 'B', 'R', 'G', 'WU', 'WB', 'WR', 'WG', 'UW', 'UB', 'UR', 'UG', 'BW', 'BU', 'BR', 'BG',
                    'RW', 'RU', 'RB', 'RG', 'GW', 'GU', 'GB', 'GR', 'WUB', 'WUR', 'WUG', 'WBU', 'WBR', 'WBG', 'WRU',
                    'WRB', 'WRG', 'WGU', 'WGB', 'WGR', 'UWB', 'UWR', 'UWG', 'UBW', 'UBR', 'UBG', 'URW', 'URB', 'URG',
                    'UGW', 'UGB', 'UGR', 'BWU', 'BWR', 'BWG', 'BUW', 'BUR', 'BUG', 'BRW', 'BRU', 'BRG', 'BGW', 'BGU',
                    'BGR', 'RWU', 'RWB', 'RWG', 'RUW', 'RUB', 'RUG', 'RBW', 'RBU', 'RBG', 'RGW', 'RGU', 'RGB', 'GWU',
                    'GWB', 'GWR', 'GUW', 'GUB', 'GUR', 'GBW', 'GBU', 'GBR', 'GRW', 'GRU', 'GRB', 'WUBR', 'WUBG', 'WURB',
                    'WURG', 'WUGB', 'WUGR', 'WBUR', 'WBUG', 'WBRU', 'WBRG', 'WBGU', 'WBGR', 'WRUB', 'WRUG', 'WRBU',
                    'WRBG', 'WRGU', 'WRGB', 'WGUB', 'WGUR', 'WGBU', 'WGBR', 'WGRU', 'WGRB', 'UWBR', 'UWBG', 'UWRB',
                    'UWRG', 'UWGB', 'UWGR', 'UBWR', 'UBWG', 'UBRW', 'UBRG', 'UBGW', 'UBGR', 'URWB', 'URWG', 'URBW',
                    'URBG', 'URGW', 'URGB', 'UGWB', 'UGWR', 'UGBW', 'UGBR', 'UGRW', 'UGRB', 'BWUR', 'BWUG', 'BWRU',
                    'BWRG', 'BWGU', 'BWGR', 'BUWR', 'BUWG', 'BURW', 'BURG', 'BUGW', 'BUGR', 'BRWU', 'BRWG', 'BRUW',
                    'BRUG', 'BRGW', 'BRGU', 'BGWU', 'BGWR', 'BGUW', 'BGUR', 'BGRW', 'BGRU', 'RWUB', 'RWUG', 'RWBU',
                    'RWBG', 'RWGU', 'RWGB', 'RUWB', 'RUWG', 'RUBW', 'RUBG', 'RUGW', 'RUGB', 'RBWU', 'RBWG', 'RBUW',
                    'RBUG', 'RBGW', 'RBGU', 'RGWU', 'RGWB', 'RGUW', 'RGUB', 'RGBW', 'RGBU', 'GWUB', 'GWUR', 'GWBU',
                    'GWBR', 'GWRU', 'GWRB', 'GUWB', 'GUWR', 'GUBW', 'GUBR', 'GURW', 'GURB', 'GBWU', 'GBWR', 'GBUW',
                    'GBUR', 'GBRW', 'GBRU', 'GRWU', 'GRWB', 'GRUW', 'GRUB', 'GRBW', 'GRBU', 'WUBRG', 'WUBGR', 'WURBG',
                    'WURGB', 'WUGBR', 'WUGRB', 'WBURG', 'WBUGR', 'WBRUG', 'WBRGU', 'WBGUR', 'WBGRU', 'WRUBG', 'WRUGB',
                    'WRBUG', 'WRBGU', 'WRGUB', 'WRGBU', 'WGUBR', 'WGURB', 'WGBUR', 'WGBRU', 'WGRUB', 'WGRBU', 'UWBRG',
                    'UWBGR', 'UWRBG', 'UWRGB', 'UWGBR', 'UWGRB', 'UBWRG', 'UBWGR', 'UBRWG', 'UBRGW', 'UBGWR', 'UBGRW',
                    'URWBG', 'URWGB', 'URBWG', 'URBGW', 'URGWB', 'URGBW', 'UGWBR', 'UGWRB', 'UGBWR', 'UGBRW', 'UGRWB',
                    'UGRBW', 'BWURG', 'BWUGR', 'BWRUG', 'BWRGU', 'BWGUR', 'BWGRU', 'BUWRG', 'BUWGR', 'BURWG', 'BURGW',
                    'BUGWR', 'BUGRW', 'BRWUG', 'BRWGU', 'BRUWG', 'BRUGW', 'BRGWU', 'BRGUW', 'BGWUR', 'BGWRU', 'BGUWR',
                    'BGURW', 'BGRWU', 'BGRUW', 'RWUBG', 'RWUGB', 'RWBUG', 'RWBGU', 'RWGUB', 'RWGBU', 'RUWBG', 'RUWGB',
                    'RUBWG', 'RUBGW', 'RUGWB', 'RUGBW', 'RBWUG', 'RBWGU', 'RBUWG', 'RBUGW', 'RBGWU', 'RBGUW', 'RGWUB',
                    'RGWBU', 'RGUWB', 'RGUBW', 'RGBWU', 'RGBUW', 'GWUBR', 'GWURB', 'GWBUR', 'GWBRU', 'GWRUB', 'GWRBU',
                    'GUWBR', 'GUWRB', 'GUBWR', 'GUBRW', 'GURWB', 'GURBW', 'GBWUR', 'GBWRU', 'GBUWR', 'GBURW', 'GBRWU',
                    'GBRUW', 'GRWUB', 'GRWBU', 'GRUWB', 'GRUBW', 'GRBWU', 'GRBUW'}

if __name__ == "__main__":
    main1 = MtgBoard()
    main1["black lotus"] = 10
    side1 = MtgBoard()
    side1["black lotus"] = 20
    print(main1)
    print(side1)
    deck1 = MtgBoard({"a": 10})
    print(deck1)
    breakpoint()
