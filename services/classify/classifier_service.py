import re

LANDUSES_KEYWORDS = {
    "annual_crops": [
        "milho", "soja", "trigo", "safra", "safrinha", "algodão", "cevada", "sorgo", "lentilha",
        "arroz", "amendoim", "girassol", "feijão", "aveia", "centeio", "ervilha", "granja"
    ],
    "perennial_crops": [
        "café", "laranja", "limão", "perene", "perenes", "citrus",  "cítricos", "abacate",
        "manga", "banana", "uva", "maçã", "pêssego", "ameixa", "abacaxi", "maracujá"
    ],
    "semiperennial_crops": [
        "cana-de-açúcar", "cana", "semiperene", "semiperenes", "semi-perene"
    ],
    "silviculture": [
        "eucalipto", "pinus", "teca", "acácia", "madeira", "silvicultura", "manejo florestal",
        "reflorestamento", "árvores", "florestamento", "plantio de árvores"
    ],
    "native_vegetation": [
        "mata nativa", "floresta", "vegetação", "área de preservação permanente", "app", "savana",
        "reservas", "reserva legal", "reserva",  "cerrado", "caatinga", "pantanal", "amazônia", "bioma",
    ],
    "dual_aptitude": [
        "dupla aptidão", "mista", "agropecuária", "cultivo e pecuária", "produção mista", "ilp",
        "dupla função", "dupla utilização", "dupla exploração", "integração lavoura-pecuária"
    ],
    "pasture": [
        "estância", "pastagem", "pasto", "gado", "capim", "braquiária", "forragem", "campo", "gramínea", "pasto cultivado",
        "cabeça", "novilho", "nelore", "bovino", "bovinos", "pecuária", "criação de gado", "pasto nativo",
    ],
    "recreation": [
        "chacará", "chácaras", "residencial", "residenciais", "restaurante", "restaurantes", "bem-estar", "evento", "eventos", 
        "festa", "festas", "lazer", "final de semana", "finais de semana", "condomínio", "condomínios", "futebol", "campo de futebol"
    ]
}

class Property:
    def __init__(
        
    ):
        pass

class Classifier:
    def __get_area_from_description(self, description:str) -> float:
        pattern = r"(\d[\d.,]*)(?:\s*)(?<!\w)(m|m²|m2|km2|km²|hectares|hect|ha|há|alqueire|alq|alqueires)\b"
        matches = re.findall(pattern, description, re.IGNORECASE)
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

    def _get_data_from_description(self, description:str) -> dict:
        cities = []
        states = []
        descriptions = []
        prices = []
        areas = []
        prices_per_ha = []
        landuses = []
        keywords = []
        improvements = []
        ad_dates = []

        area = self.__get_area_from_description(description)


if __name__ == "__main__":
    pass