import unittest

from MtgScraper import AetherhubScraper, MtgGoldfishScraper, MtgaZoneScraper, MtgBoard


class TestMtgGoldfish(unittest.TestCase):
    def setUp(self):
        self.scraper = MtgGoldfishScraper()

    def tearDown(self):
        self.scraper.close_session()

    def test_goldfish(self):
        example_deck = "https://www.mtggoldfish.com/deck/7020859#paper"
        m = MtgBoard(
            {'Brainstorm': 4, 'Brazen Borrower': 2, 'Daze': 4, 'Fatal Push': 3, 'Flooded Strand': 1, 'Force of Will': 4,
             'Go for the Throat': 1, 'Island': 1, 'Kaito, Bane of Nightmares': 2, 'Marsh Flats': 1,
             'Murktide Regent': 2, 'Nethergoyf': 3, 'Orcish Bowmasters': 3, 'Polluted Delta': 4, 'Ponder': 4,
             'Scalding Tarn': 1, 'Spell Pierce': 2, 'Swamp': 1, 'Tamiyo, Inquisitive Student': 4, 'Thoughtseize': 3,
             'Undercity Sewers': 1, 'Underground Sea': 4, 'Verdant Catacombs': 1, 'Wasteland': 4})
        s = MtgBoard({'Barrowgoyf': 2, 'Blue Elemental Blast': 2, 'Consign to Memory': 2, 'Flusterstorm': 1,
                      'Force of Negation': 2, 'Go for the Throat': 1, "Grafdigger's Cage": 1,
                      'Harbinger of the Seas': 1, 'Null Rod': 1, 'Surgical Extraction': 2})
        main, side = self.scraper.scrape_page(example_deck)
        self.assertEqual(m, main)
        self.assertEqual(s, side)


class TestMtgaZone(unittest.TestCase):
    def setUp(self):
        self.scraper = MtgaZoneScraper()

    def tearDown(self):
        self.scraper.close_session()

    def test_mtgazone(self):
        std_decks = self.scraper.scrape_format("standard")
        self.assertTrue(std_decks)

class TestAetherhubScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = AetherhubScraper()

    def tearDown(self):
        self.scraper.close_session()

    def test_aetherhub_page(self):
        m = MtgBoard({'Bristly Bill, Spine Sower': 1, 'Bite Down': 1, "Innkeeper's Talent": 1, "Archdruid's Charm": 1,
                    'Snakeskin Veil': 1, 'Tail Swipe': 1, "Hunter's Talent": 1, 'Tribute to the World Tree': 1,
                    "Garruk's Uprising": 1, 'Frantic Strength': 1, 'Pick Your Poison': 1, "Animist's Might": 1,
                    'Leaping Ambush': 1, 'Heaped Harvest': 1, 'Map the Frontier': 1, 'Case of the Locked Hothouse': 1,
                    'Doubling Season': 1, 'Swiftfoot Boots': 1, 'Gruff Triplets': 1, 'Llanowar Loamspeaker': 1,
                    'Tender Wildguide': 1, 'Kami of Whispered Hopes': 1, 'Nissa, Resurgent Animist': 1,
                    'Lumra, Bellow of the Woods': 1, 'Goldvein Hydra': 1, 'Bristlepack Sentry': 1, 'Wildwood Scourge': 1,
                    'Llanowar Elves': 1, 'Mossborn Hydra': 1, 'Springbloom Druid': 1, 'Rampaging Baloths': 1,
                    'Nessian Hornbeetle': 1, 'Invasion of Zendikar // Awakened Skyclave': 1, 'Nissa, Ascended Animist': 1,
                    'Vivien Reid': 1, 'Forest': 21, "Rogue's Passage": 1, 'Fabled Passage': 1, 'Evolving Wilds': 1,
                    'Terramorphic Expanse': 1})
        brawl_deck = self.scraper.scrape_page("https://aetherhub.com/Metagame/Brawl/Deck/bristly-bill-spine-sower-1164422")
        self.assertEqual(m, brawl_deck.mainboard)
        self.assertEqual({}, brawl_deck.sideboard)

if __name__ == '__main__':
    unittest.main()
