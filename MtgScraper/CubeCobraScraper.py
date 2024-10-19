import json
from collections import Counter
from typing import Iterable

import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm


class CubeCobraScraper:
    def __init__(self, session=None, url=None):
        if session is None:
            self.session = requests.Session()
        else:
            self.session = session
        if url:
            self.cubes = self.get_cube_dict(url=url)
        else:
            self.cubes = self.get_cube_dict()

    def to_file(self, filepath: str = "../cubecobra.py"):
        result = dict()
        for name, cube_cobra_id in tqdm(self.cubes.items()):
            result[name] = self.fetch_cube_list(self, cube_cobra_id)
        with open(filepath, "w") as f:
            f.write("Cube = " + str(result))

    def get_cube_dict(self, url: str = "https://cubecobra.com/explore") -> dict[str, str]:
        """
        Return {cube_name: cube_list, ...}. If url not provided, gets most popular cubes.
        """
        response = self.session.get(url)
        text = response.text
        soup = BeautifulSoup(text, 'lxml')
        # Find the script tag that contains the dictionary and get the text
        script_content = soup.find('script', string=lambda t: t and 'window.reactProps' in t).string
        # remove var name and trailing ;
        json_str = script_content.split('window.reactProps =', 1)[1].rsplit(';', 1)[0].strip()

        cubes_list: dict = json.loads(json_str)
        if "popular" in cubes_list:
            cubes_list = cubes_list["popular"]
        else:
            cubes_list = cubes_list["cubes"]
        # Access the data in the dictionary
        return {CubeCobraScraper.build_name(el): el['id'] for el in cubes_list}

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
        """
        Hydrate Cube Name with Cube's Category to make cube name clear.
        """
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
    scraper = CubeCobraScraper(url="https://cubecobra.com/explore")
    scraper.to_file()
