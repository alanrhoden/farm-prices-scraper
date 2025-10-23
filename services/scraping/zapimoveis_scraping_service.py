from bs4 import BeautifulSoup
from pandas import DataFrame

from services.advertising.advertising import Advertising
from services.scraping.scraper import Scraper
from services.url.zapimoveis_url_service import ZapImoveisUrlService
from css_selectors.zapimoveis_selectors import *

class ZapImoveisScraper(Scraper):
    def __init__(self):
        super().__init__()
        self.url_service = ZapImoveisUrlService()

    def _get_number_of_properties(self, base_url:str) -> int:
        page = self.request_page(base_url)
        element = self._safe_select(page, NUMBER_OF_PROPERTIES)
        num_of_properties = int(element[0].text.split(" ")[0].replace(".", ""))
        
        return num_of_properties
    
    def get_number_of_pages(self, base_url:str) -> int:
        ads_per_page = 30
        num_of_properties = self._get_number_of_properties(base_url)
        num_of_pages = (num_of_properties//ads_per_page) + 1
        
        return num_of_pages
    
    def get_ad_links(self, urls:list) -> list:
        ads = []

        for u in urls:
            page = self.request_page(u)
            cards = self._safe_select(page, AD_CARD)

            for c in cards:
                try:
                    anchor_tag = c.select("a")[0]
                    href = anchor_tag["href"]
                    ads.append(href)
                except:
                    #TODO: process properties with multiple ads
                    pass
        
        return ads
    
    def _get_area(self, page:BeautifulSoup) -> float | None:
        area = self._get_text(page, PROPERTY_AREA)
        if not area:
            return None
        area = area.replace(" m²", "")
        area = float(area)
        area = area / 10000

        return area
    
    def _get_price(self, page:BeautifulSoup) -> float | None:
        price = self._get_text(page, PROPERTY_PRICE)
        if not price:
            return None
        price = price.replace("R$ ", "")
        price = price.replace(".", "")
        price = float(price)
        
        return price

    def _get_description(self, page:BeautifulSoup) -> str | None:
        description = self._get_text(page, DESCRIPTION)
        if not description:
            return None
        return description

    def _get_ad_date(self, page:BeautifulSoup) -> str | None:
        ad_date = self._get_text(page, AD_DATE)
        if not ad_date:
            return None
        return ad_date

    def get_ad(self, ad_url:str, city:str, state:str) -> Advertising:
        page = self.request_page(ad_url)
        area = self._get_area(page)
        price = self._get_price(page)
        description = self._get_description(page)
        ad_date = self._get_ad_date(page)

        ad = Advertising(city, state, price, area, description, ad_date, ad_url)

        return ad
    
    def run(self, city:str, state:str) -> dict:
        base_url = self.url_service.base_url(city, state)
        num_of_pages = self.get_number_of_pages(base_url)
        urls = self.url_service.build_urls(base_url, num_of_pages)
        ad_urls = self.get_ad_links(urls)
        ads = []

        for url in ad_urls:
            ad = self.get_ad(url, city, state)
            ads.append(ad)

        return ads


if __name__ == "__main__":
    pass