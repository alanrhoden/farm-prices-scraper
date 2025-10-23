import pandas as pd
import urllib3

from services.scraping.zapimoveis_scraping_service import ZapImoveisScraper

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

city, state = "Correntina", "Bahia"

zap_scraper = ZapImoveisScraper()
res = zap_scraper.run(city, state)

for ad in res:
    ad.update_data_by_description()
