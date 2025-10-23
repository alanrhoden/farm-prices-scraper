import re

class Advertising:
    def __init__(
        self,
        city: str,
        state: str,
        price: str,
        area: str,
        description: str,
        ad_date: str,
        url: str
    ):
        self.city = city
        self.state = state
        self.price = price
        self.area = area
        self.price_per_ha = None
        self.description = description
        self.ad_date = ad_date
        self.url = url
        self.landuses = None

    def _get_landuses_from_description(self) -> None:
        if not self.description:
            return None
        
        keywords = {
            "annual_crops": [
                "milho", "soja", "trigo", "safra", "safrinha", "algodão", "cevada", "sorgo", "lentilha",
                "arroz", "amendoim", "girassol", "feijão", "aveia", "centeio", "ervilha", "granja",
                "floricultura", "horticultura",
            ],
            "perennial_crops": [
                "café", "laranja", "limão", "perene", "perenes", "citrus",  "cítricos", "abacate",
                "manga", "banana", "uva", "maçã", "pêssego", "ameixa", "abacaxi", "maracujá",
                "fruticultura", "vinicultura"
            ],
            "semiperennial_crops": [
                "cana-de-açúcar", "cana", "semiperene", "semiperenes", "semi-perene"
            ],
            "silviculture": [
                "eucalipto", "pinus", "teca", "acácia", "madeira", "silvicultura", "manejo florestal",
                "reflorestamento", "árvores", "florestamento", "plantio de árvores"
            ],
            "native_vegetation": [
                "savana", "mata nativa", "floresta", "vegetação", "agrofloresta", "agroecologia",
                "área de preservação permanente", "area de preservacao permanente","app",
                "reservas", "reserva legal", "reserva", "bioma",
                "amazônia", "amazonia", "caatinga", "cerrado", "pampa", "pantanal"
            ],
            "dual_aptitude": [
                "dupla aptidão", "mista", "agropecuária", "cultivo e pecuária", "cultivo e pecuaria",
                "pecuária e cultivo", "pecuaria e cultivo", "produção mista", "ilp",
                "dupla função", "dupla utilização", "dupla exploração", "integração lavoura-pecuária",
                "agroindústria", "agroindustria"
            ],
            "pasture": [
                "estância", "estancia", "pastagem", "pasto", "gado", "capim", "braquiária", "forragem", "campo", "gramínea", 
                "pasto cultivado", "cabeça", "novilho", "nelore", "bovino", "bovinos", "pecuária", "criação de gado", 
                "pasto nativo",
            ],
            "recreation": [
                "chacará", "chácaras", "residencial", "residenciais", "restaurante", "restaurantes", "bem-estar", 
                "evento", "eventos", "festa", "festas", "lazer", "final de semana", "finais de semana", 
                "condomínio", "condomínios", "futebol", "campo de futebol"
            ]
        }

        landuses = {}
        desc = self.description.lower()

        for lulc, kw_list in keywords.items():
            for word in kw_list:
                if word in desc:
                    landuses.setdefault(lulc, []).append(word)
        
        return landuses if landuses else None
        
    def _get_area_from_description(self) -> float:
        pattern = r"(\d[\d.,]*)(?:\s*)(?<!\w)(m|m²|m2|km2|km²|hectares|hect|ha|há|alqueire|alq|alqueires)\b"
        matches = re.findall(pattern, self.description, re.IGNORECASE)
        max_area = 0

        for match in matches:
            number_str = match[0].replace(".", "").replace(",", ".")
            number = float(number_str)
            unit = match[1].lower()

            if unit in ["hectares", "hect", "ha", "há"]:
                number *= 10000
            elif unit in ["km2", "km²"]:
                number *= 1000000
            elif unit in ["alqueire", "alq", "alqueires"]:
                number *= 24200

            if number > max_area:
                max_area = number

        return max_area
    
    def _get_price_from_description(self) -> float | None:
        if not self.description:
            return None

        desc = self.description.lower()
        prices: list[float] = []

        def parse_number(num_str: str) -> float | None:
            s = num_str.strip()
            # handle both thousands '.' and decimal ','
            if '.' in s and ',' in s:
                s = s.replace('.', '').replace(',', '.')
            else:
                s = s.replace('.', '').replace(',', '.')
            try:
                return float(s)
            except ValueError:
                return None

        # 1) explicit currency like "R$ 1.200.000,00"
        for m in re.findall(r"r\$\s*[\d\.\,]+", desc):
            num = re.search(r"[\d\.\,]+", m)
            if num:
                v = parse_number(num.group(0))
                if v is not None:
                    prices.append(v)

        # 2) words like "valor", "preço", "preco", "venda" followed by a number (with optional R$)
        for m in re.findall(r"(?:valor|preço|preco|venda)\s*(?:[:\-\s])?\s*r?\$?\s*([\d\.\,]+)", desc):
            v = parse_number(m)
            if v is not None:
                prices.append(v)

        # 3) numbers with scale words (mil, mi, milhão(s), milhões)
        for num_str, unit in re.findall(r"([\d\.,]+)\s*(milhões|milhao|milhoes|milhão|mi|mil|m)\b", desc):
            v = parse_number(num_str)
            if v is None:
                continue
            unit = unit.replace("ã","a")
            if unit.startswith("milhão") or unit in ("milhoes", "mi"):
                v *= 1_000_000
            elif unit in ("mil", "m"):
                v *= 1_000
            prices.append(v)

        if not prices:
            return None

        # choose the largest detected price (most likely the total property price)
        return max(prices)

    def update_data_by_description(self):
        area = self._get_area_from_description()
        price = self._get_price_from_description()
        landuses = self._get_landuses_from_description()

        if area == self.area:
            print("Ad area matches description.")
        else:
            print("Ad area doesnt match description.")
            print(f"\tAd area: {self.area}")
            print(f"\tDescription area: {area}")

        if price == self.price:
            print("Ad price matches description.")
        else:
            print("Ad price doesnt match descrption.")
            print(f"\tAd price: {self.price}")
            print(f"\tDescription price: {price}")