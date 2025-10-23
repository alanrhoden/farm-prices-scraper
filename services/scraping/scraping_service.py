import re

from random import choice
from requests import Session
from time import sleep
from bs4 import BeautifulSoup, ResultSet

class Scraper:
    def __init__(self):
        self.headers = {
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        }
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
        ]

    def request_page(self, url:str) -> BeautifulSoup:
        sleep(1)
        headers = self.headers.copy()
        headers["User-Agent"] = choice(self.user_agents)
        page = Session().get(url, headers=headers, verify=False)
        soup = BeautifulSoup(page.text, "html.parser")

        return soup

    def _safe_select(self, page:BeautifulSoup, selector:str) -> ResultSet | None:
        element = page.select(selector)
        if not element:
            print(f"Unable to find element:\n\t{selector}")
            return None
        
        return element

    def _get_text(self, page:BeautifulSoup, selector:str) -> str | None:
        element = self._safe_select(page, selector)
        if not element:
            return None
        text = element[0].text

        return text


if __name__ == "__main__":
    pass