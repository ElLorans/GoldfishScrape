import logging
from abc import ABC, abstractmethod
from typing import Any, Optional, Iterable, Literal

import requests
from bs4 import BeautifulSoup
from requests import Session
from tqdm.auto import tqdm

from MtgScraper.mtg_utils import MtgDeck, UNCLEAR_DECK_NAMES

MtgSources = Literal["MtgGoldfish", "MtgaZone", "Aetherhub"]
FormatName = Literal[
    'Standard', 'Alchemy', 'Timeless', 'Historic', 'Brawl', 'Historic Brawl', "Explorer", 'Pioneer', 'Modern', 'Legacy', 'Pauper', 'Commander', "Duel Commander", "Penny Dreadful", "Vintage"]
FormatNameLower = Literal[
    'standard', 'alchemy', 'timeless', 'historic', 'brawl', 'historic brawl', "explorer", 'pioneer', 'modern', 'legacy', 'pauper', 'commander', 'duel commander', "penny dreadful", "vintage"]


class MtgScraper(ABC):
    """
    Abstract Base Class for scraping Magic: The Gathering decklist websites.
    Subclasses must implement the abstract methods to provide site-specific scraping logic.

    Class Attributes:
        base_url (str): The base URL of the target website.
        allowed_formats (frozenset(str)): the allowed formats to scrape in lowercase.
    Instance Attributes:
        session (None | requests.Session): A requests session object for making HTTP requests.
                                   Can be used for connection pooling, setting headers, etc.
        clean: if decks with names such as WBRG must be included
        fullness: implemented by MtgGoldfish, set to False if you do not need decks after 'View More'
    Process:
        scrape_formats -> scrape_format -> build_url_format
                                      | -> get_soup -> fetch_links -> fetch_all_links
                                      | -> scrape_page
    """
    base_url: str
    allowed_formats: set[FormatNameLower]

    def __init__(self, session: None | Session = None, clean: bool = True, fullness: bool = True) -> None:
        self.session: Session = Session() if session is None else session
        self.clean = clean
        self.fullness = fullness

    @abstractmethod
    def translate_format_name(self, string: str) -> str:
        """
        In case format name needs to be converted.
        """
        return string.lower().replace(' ', '_')

    @abstractmethod
    def build_url_format(self, formato: str) -> str:
        formato = self.translate_format_name(formato)
        return f"{self.base_url}/{formato}" if not formato.startswith(self.base_url) else formato

    @abstractmethod
    def fetch_all_links(self, soup: BeautifulSoup) -> dict[str, str]:
        pass

    @abstractmethod
    def scrape_page(self, url: str) -> MtgDeck:
        """
        Scrapes a single page URL to extract decklist information.
        Args:
            url (str): The absolute URL of the decklist page to scrape.
        """
        pass

    def fetch_links(self, soup: BeautifulSoup) -> dict[str, str]:
        if self.fullness:
            return self.fetch_all_links(soup)
        return {k: v for k, v in self.fetch_all_links(soup).items() if k not in UNCLEAR_DECK_NAMES}

    def get_soup(self, url: str, **params: dict[str, Any]) -> None | BeautifulSoup:
        """
        Helper method to fetch HTML content from a URL and parse it with BeautifulSoup.

        Args:
            url (str): The URL to fetch.
            params (Optional[dict[str, Any]]): Optional dictionary of URL parameters.

        Returns:
            Optional[BeautifulSoup]: A BeautifulSoup object representing the parsed HTML,
                                     or None if the request failed or returned non-200 status.
        """
        params = params or dict(headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9", "Connection": "keep-alive"})
        try:
            response = self.session.get(url, **params)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            soup = BeautifulSoup(response.text, 'lxml')
            return soup
        except requests.exceptions.RequestException as exc:
            print(f"Error fetching URL {url}: {exc}")
            return None
        except Exception as exc:
            print(f"Error parsing URL {url}: {exc}")
            return None

    def scrape_formats(self, formats: Iterable[str]) -> tuple[dict[str, MtgDeck], ...]:
        if isinstance(formats, str):
            formats = (formats,)
        return tuple(self.scrape_format(formato) for formato in formats)

    def scrape_format(self, formato: str, **params: dict[str, Any]) -> dict[str, MtgDeck]:
        edited_formato = self.translate_format_name(formato)
        if edited_formato not in self.allowed_formats:
            logging.error(f"Format {formato} is not supported")
            return {}
        decks: dict[str, MtgDeck] = {}
        soup = self.get_soup(self.build_url_format(formato), **params)
        links = self.fetch_links(soup)
        for name, link in tqdm(links.items(), position=0, leave=True):
            decks[name] = self.scrape_page(link)
        return decks

    def close_session(self):
        """Closes the underlying requests session."""
        self.session.close()
