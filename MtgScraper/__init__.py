# init


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
    def __init__(self, mainboard=None, sideboard=None):
        if mainboard is None:
            self.mainboard = MtgBoard()
        else:
            self.mainboard = mainboard

        if sideboard is None:
            self.sideboard = MtgBoard()
        else:
            self.sideboard = mainboard


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

        # Double Face Cards
        'mistgate pathway': 'hengegate pathway // mistgate pathway',
        'grimclimb pathway': 'brightclimb pathway // grimclimb pathway',
        'agadeem, the undercrypt': "agadeem's awakening // agadeem, the undercrypt"
    }

    for k, v in replacements.items():
        result = stringa.replace(k, v)
    return result


if __name__ == "__main__":
    a = MtgBoard()
    breakpoint()
