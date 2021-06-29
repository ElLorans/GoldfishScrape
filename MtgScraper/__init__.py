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


if __name__ == "__main__":
    a = MtgBoard()
    breakpoint()
