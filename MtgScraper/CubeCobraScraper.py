import json
from collections import Counter
from typing import Iterable

import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm


class CubeCobraScraper:
    def __init__(self, session=None):
        if session is None:
            self.session = requests.Session()
        else:
            self.session = session
        result = dict()
        with self.session as connection:
            self.cubes = self.get_cube_dict()
            for name, cube_cobra_id in tqdm(self.cubes.items()):
                result[name] = self.fetch_cube_list(self, cube_cobra_id)
        with open("cubecobra.py", "w") as f:
            f.write("Cube = " + str(result))

    def get_cube_dict(self) -> dict[str, str]:
        # query "" and order by popularity
        url = "https://cubecobra.com/search/%22%22/0?order=pop"

        response = self.session.get(url)
        text = response.text
        soup = BeautifulSoup(text, 'lxml')
        # Find the script tag that contains the dictionary
        script = soup.find('script', type='text/javascript', text=lambda t: t.startswith('window.reactProps'))

        # Extract the dictionary from the script tag
        start = script.text.index('[{')
        end = script.text.index('}]') + 2
        cubes_data = script.text[start:end]
        cubes_list: list[dict[str, str]] = json.loads(script.text[start:end])
        # Access the data in the dictionary
        return {CubeCobraScraper.build_name(el): el['_id'] for el in cubes_list}

    @staticmethod
    def fetch_cube_list(self, cube_id, session=None) -> dict[str, int]:
        if session is None:
            session = self.session
        else:
            session = session
        url: str = "https://cubecobra.com/cube/api/cubelist/{}".format(cube_id)
        response = session.get(url)
        cube_list: list[str] = response.text.split('\n')
        cube_dict: dict[str, int] = dict(Counter(cube_list))
        return cube_dict

    @staticmethod
    def build_name(cube_dictionary: dict) -> str:
        name: str = cube_dictionary['name']
        name_sources: tuple[str, ...] = ('categoryPrefixes', 'categoryOverride')

        sub_name: str = "("
        for source in name_sources:
            # if key is in dict, key is not empty, and value is not already in name (avoid repetitions in name)
            val = cube_dictionary.get(source)
            if val:
                if isinstance(val, str) and val not in cube_dictionary['name']:
                    sub_name += val + " "
                elif isinstance(val, Iterable):
                    for el in val:
                        if el not in cube_dictionary['name'] and el not in name:
                            sub_name += el + " "
        if sub_name != "(":
            name += f" {sub_name[:-1]})"
        return name


if __name__ == "__main__":
    scraper = CubeCobraScraper()
