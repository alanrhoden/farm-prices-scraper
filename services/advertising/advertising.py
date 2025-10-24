import re

from uuid import uuid4

class Advertising:
    def __init__(
        self,
        ad_code: str,
        city: str,
        state: str,
        area: str,
        price: str,
        description: str,
        ad_date: str,
        url: str
    ):
        self.id = str(uuid4())
        self.ad_code = ad_code
        self.city = city
        self.state = state
        self.area = area
        self.price = price
        self.price_per_ha = None
        self.description = description
        self.description_price = None
        self.landuses = None
        self.ad_date = ad_date
        self.url = url

    def __repr__(self):
        text = f"""
        Advertising {self.id}:
            Advertising code: {self.ad_code}
            City: {self.city.capitalize()}, {self.state.capitalize()}
            Price: R$ {self.price:.2f}
            Area: {self.area:.2f} ha
            Description price: R$ {self.description_price}
            Landuses: {self.landuses}
            Url: {self.url}
        """

        return text.strip()


class AdvertisingParser:
    def __init__(self):
        pass

    def _get_landuses_from_description(self, description:str) -> dict|None:
        if not description:
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
        desc = description.lower()

        for lulc, kw_list in keywords.items():
            for word in kw_list:
                if word in desc:
                    landuses.setdefault(lulc, []).append(word)
        
        return landuses if landuses else None
        
    def _get_price_from_description(self, description:str) -> float|None:
        if not description:
            return None

        desc = description.lower()
        prices: list[float] = []

        def parse_number(num_str: str) -> float|None:
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

    def __get_area_from_description(self, description: str) -> float | None:
        if not description:
            return None

        desc = description.lower()

        pattern = r"""
            (?P<num>\d{1,3}(?:[.\s]\d{3})*(?:,\d+)?|\d+(?:[.,]\d+)?)   # number with possible thousand separators
            (?:\s*(?P<scale>milhões|milhao|milhoes|milhão|mi|mil))?   # optional scale word (mil, milhão)
            (?:\s*(?:a|–|-)\s*(?P<num2>\d{1,3}(?:[.\s]\d{3})*(?:,\d+)?|\d+(?:[.,]\d+)?))?  # optional range second number
            \s*
            (?P<unit>m2|m²|m 2|m ²|m\b|km2|km²|km 2|ha|hectares|héctares|hect|HECT|alqueire|alqueires|alq)\b
        """

        def norm_number(s: str) -> float:
            s = s.strip().replace(" ", "")
            # If both '.' and ',' present -> '.' is thousands, ',' is decimal
            if "." in s and "," in s:
                s = s.replace(".", "").replace(",", ".")
            else:  # otherwise remove thousands-sep dots and convert comma decimal to dot
                s = s.replace(".", "").replace(",", ".")
            return float(s)

        matches = re.finditer(pattern, desc, flags=re.IGNORECASE | re.VERBOSE)
        max_area_ha = 0.0

        for m in matches:
            try:
                n1 = norm_number(m.group("num"))
            except Exception:
                continue

            # if there's a range, take the larger number
            if m.group("num2"):
                try:
                    n2 = norm_number(m.group("num2"))
                    n = max(n1, n2)
                except Exception:
                    n = n1
            else:
                n = n1

            scale = m.group("scale") or ""
            if scale:
                scale = scale.replace("ã", "a")
                if scale.startswith("milhao") or scale in ("milhoes", "mi"):
                    n *= 1_000_000
                elif scale in ("mil", "m"):
                    n *= 1_000

            unit = (m.group("unit") or "").lower().replace(" ", "")
            # convert to hectares
            if unit in ("m2", "m²", "m", "m2", "m 2", "m ²"):
                # number given in square meters
                area_ha = n / 10000.0
            elif unit.startswith("km"):
                # km² -> 1 km² = 100 ha
                area_ha = n * 100.0
            elif unit.startswith("hect") or unit in ("ha", "há"):
                area_ha = n
            elif unit in ("alqueire", "alqueires", "alq"):
                # approximate: 1 alqueire ≈ 2.42 ha (adjust if you need a different region's value)
                area_ha = n * 2.42
            else:
                continue

            if area_ha > max_area_ha:
                max_area_ha = area_ha

        return max_area_ha if max_area_ha > 0 else None

    def _rectify_area(self, ad:Advertising) -> float:
        desc_area = self.__get_area_from_description(ad.description)

        if desc_area is None:
            return ad.area
        
        if ad.area is None:
            return desc_area

        max_area = max(ad.area, desc_area)

        return max_area

    def _rectify_price(self, ad:Advertising) -> float:
        pass

    def parse(self, ad_data:dict):
        ad = Advertising(
            ad_data["ad_code"],
            ad_data["city"],
            ad_data["state"],
            ad_data["area"],
            ad_data["price"],
            ad_data["description"],
            ad_data["ad_date"],
            ad_data["url"]
        )

        desc_price = self._get_price_from_description(ad.description)

        ad.landuses = self._get_landuses_from_description(ad.description)
        ad.area = self._rectify_area(ad)
        ad.description_price = desc_price

        return ad

