"""
class MtgBoard
class MtgDeck
func clean_database
"""
import itertools
from typing import Final

MTG_COLORS: Final[list[str]] = ['W', 'R', 'U', 'G', 'B']

# names not to be considered (e.g.: W, WR, GB, GBRU)
UNCLEAR_DECK_NAMES: Final[frozenset[str]] = frozenset(
    ''.join(perm) for r in range(1, len(MTG_COLORS) + 1) for perm in itertools.permutations(MTG_COLORS, r))


class MtgBoard(dict[str, int]):
    """
    Acts as a Dict[str, int] that accepts only str as keys and int as values.
    """
    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError("Key should be str, not", type(key))
        if not isinstance(value, int):
            raise TypeError("Key should be int, not", type(value))
        super().__setitem__(key, value)

    @classmethod
    def from_text(cls, stringa: str) -> "MtgBoard":
        deck_list = MtgBoard()
        for line in stringa.splitlines():
            if len(line.strip()) > 0:
                copies, card = line.split(' ', 1)
                card = card.split('[')[0].split('<')[0].strip()
                deck_list[card] = deck_list.get(card, 0) + int(copies)
        return deck_list

    def count(self) -> int:
        result = 0
        for k, v in self.items():
            result += v
        return result

class MtgDeck:
    """
    A class with 2 attributes that act as Dict[str, int]: mainboard and sideboard.
    """

    def __init__(self, mainboard: None | MtgBoard = None, sideboard: None | MtgBoard = None):
        self.mainboard = MtgBoard() if mainboard is None else mainboard
        self.sideboard = MtgBoard() if sideboard is None else sideboard

    def __repr__(self):
        return f"Mainboard: {self.mainboard}\nSideboard: {self.sideboard}"

    def __iter__(self):
        # Allow unpacking into two variables
        return iter((self.mainboard, self.sideboard))

    def __setitem__(self, key, value):
        if key == 0:
            self.mainboard = value
        elif key == 1:
            self.sideboard = value
        else:
            raise TypeError("Key should be 0 or 1, not", key)



def clean_database(stringa: str) -> str:
    replacements = {  # Dream-Den and Lim-Dûl are misspelled on Goldfish
        "Dream Den": "Dream-Den", "Lim-Dul": "Lim-Dûl", "Lim-D�l": "Lim-Dûl",

        # Change Godzilla names
        "Dorat, the Perfect Pet": "Sprite Dragon", "Mothra, Supersonic Queen": "Luminous Broodmoth",
        'Gigan, Cyberclaw Terror': 'Gyruda, Doom of Depths', 'Babygodzilla, Ruin Reborn': 'Pollywog Symbiote',
        'Anguirus, Armored Killer': 'Gemrazer', 'Bio-Quartz Spacegodzilla': 'Brokkos, Apex of Forever',
        'Godzilla, Doom Inevitable': 'Yidaro, Wandering Monster',
        'Godzilla, King of the Monsters': 'Zilortha, Strength Incarnate', 'Godzilla, Primeval Champion': 'Titanoth Rex',

        # correct Goldfish mistakes and Alchemy cards since they are not supported
        ' <292 C>': '', ' [RNA]': '', ' [mps]': '', '\n\nReport Deck Name': '', ' [GRN]': '',
        "A - Oran - Rief Ooze": "Oran-Rief Ooze", "a-Dragon's Rage Channeler": "Dragon's rage channeler",
        "Sakurtribe Elder": "Sakura-Tribe Elder",
        "a-The One Ring": "The One Ring",
        "a-Mentor's Guidance": "Mentor's Guidance",
        "Clavileno, First of the Blessed": "Clavileño, First of the Blessed",

        # Double Face Cards
        'Mistgate Pathway': 'Hengegate Pathway // Mistgate Pathway',
        'Grimclimb Pathway': 'Brightclimb Pathway // Grimclimb Pathway',
        'Agadeem, the Undercrypt': "Agadeem's Awakening // Agadeem, the Undercrypt", 'Pick-Beeble': 'Pick-a-Beeble',
        'Lagonnband Trailblazer': 'Lagonna-Band Trailblazer', 'Sedasher Octopus': 'Sea-Dasher Octopus',

        '///': '//',

        # LOTR accents
        "Gloin, Dwarf Emissary": "Glóin, Dwarf Emissary", "Smeagol, helpful guide": "Sméagol, helpful guide",
        "Palantir of Orthanc": "Palantír of Orthanc", "Lord of the Nazgul": "Lord of the Nazgûl",
        "Troll of Khazad-dum": "Troll of Khazad-dûm", "Lorien Revealed": "Lórien Revealed",
        "Anduril, Flame of the West": "Andúril, Flame of the West", "Mauhur": "Mauhúr", "Barad-dur": "Barad-dûr",
        'Eomer, King of Rohan': 'Éomer, King of Rohan', 'Eowyn, Shieldmaiden': 'Éowyn, Shieldmaiden',
        'Theoden, King of Rohan': 'Théoden, King of Rohan',
        'Gilraen, Dunedain Protector': 'Gilraen, Dúnedain Protector',
        'Haldir, Lorien Lieutenant': 'Haldir, Lórien Lieutenant', 'Lothlorien Lookout': 'Lothlórien Lookout',
        'Soothing of Smeagol': 'Soothing of Sméagol',

        "Bartolome del Presidio": "Bartolomé del Presidio",

        # Alchemy
        "A-Haywire Mite": "Haywire Mite", "A-Cauldron Familiar": "Cauldron Familiar",
        "A-The Meathook Massacre": "The Meathook Massacre", }

    for k, v in replacements.items():
        stringa = stringa.replace(k, v)
    return stringa


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
