from bs4 import BeautifulSoup
from pandas import DataFrame

from services.scraping.scraping_service import Scraper
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
            return None, None
        price = price.replace("R$ ", "")
        price = price.replace(".", "")
        price = float(price)
        price_per_ha = price / 10000
        
        return price, price_per_ha

    def get_ad_info(self, ad_url: str) -> dict:
        page = self.request_page(ad_url)
        area = self._get_area(page)
        price, price_per_ha = self._get_price(page)
        description = self._get_text(page, DESCRIPTION)
        results = {
            "city": "",
            "state": "",
            "price": price,
            "area": area,
            "description": description,
            "ad_date": "",
            "url": ad_url
        }

        return results
    
    def run(self, city:str, state:str) -> DataFrame:
        base_url = self.url_service.base_url(city, state)
        num_of_pages = self.get_number_of_pages(base_url)
        urls = self.url_service.build_urls(base_url, num_of_pages)
        ad_urls = self.get_ad_links(urls)
        print(ad_urls)


if __name__ == "__main__":
    pass