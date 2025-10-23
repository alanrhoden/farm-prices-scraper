from services.url.urls_service import UrlService

class ZapImoveisUrlService(UrlService):
    def __init__(self):
        super().__init__()

    def _path(self, city:str, state:str) -> str:
        city = city.lower().replace(" ", "-")
        city = self.remove_signs(city)
        state_acronym = self.get_state_acronym(state).lower()
        path = f"venda/fazendas-sitios-chacaras/{state_acronym}+{city}"

        return path

    def __location_parameters(self, city:str, state:str) -> str:
        city = self.capitalize(city).replace(" ", "+")
        city = self.remove_signs(city)
        state = self.capitalize(state).replace(" ", "+")
        state = self.remove_signs(state)
        params = f"onde=%2C{state}%2C{city}%2C%2C%2C%2C%2Ccity%2CBR%3E{state}%3ENULL%3E{city}%2C0.000000%2C0.000000%2C"

        return params

    def _query_string(self, city:str, state: str) -> str:
        transaction = "transacao=venda"
        property_type = "tipos=granja_residencial"
        location_params = self.__location_parameters(city, state)
        query_str = f"?{transaction}&{property_type}&{location_params}"

        return query_str

    def base_url(self, city:str, state: str) -> str:
        domain = "https://www.zapimoveis.com.br"
        path = self._path(city, state)
        query_str = self._query_string(city, state)
        url = f"{domain}/{path}/{query_str}"

        return url
    
    def build_urls(self, base_url:str, number_of_pages:int) -> list:
        pages = []
        pages.append(base_url)

        for p in range(number_of_pages):
            if p != 0:
                url = base_url.replace("&tipos=granja_residencial&", f"&tipos=granja_residencial&pagina={p+1}&")
                pages.append(url)
        
        return pages


if __name__ == "__main__":
    pass