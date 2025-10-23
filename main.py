import pandas as pd
import urllib3

from services.url.zapimoveis_url_service import ZapImoveisUrlService
from services.scraping.zapimoveis_scraping_service import ZapImoveisScraper

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

zap_url_service = ZapImoveisUrlService()
zap_scraper = ZapImoveisScraper()

city, state = "Porto Alegre", "Rio Grande do Sul"

base_url = zap_url_service.base_url(city, state)
num_of_pages = zap_scraper.get_number_of_pages(base_url)
pages = zap_url_service.build_urls(base_url, num_of_pages)
ads = zap_scraper.get_ads(pages)

results = []


counter = 0
for ad in ads:
    counter += 1
    print(f"Processing ad number: {counter}")
    ad_info = zap_scraper.get_ad_info(ad)
    results.append(ad_info)

df = pd.DataFrame.from_dict(results)

df.to_excel(f"ad_data_{city}_{state}.xlsx")