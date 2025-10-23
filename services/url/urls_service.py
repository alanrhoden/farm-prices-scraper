from unicodedata import normalize, combining

class UrlService:
    def __init__(self):
        pass

    def remove_signs(self, text:str) -> str:
        return "".join(
            c for c in normalize("NFKD", text)
            if not combining(c)
        )
    
    def capitalize(self, text:str, capitalize_prepositions:bool=False) -> str:
        prepositions = {"do", "da", "dos", "das", "de", "e", "em", "no", "na", "nos", "nas"}
        words = text.lower().split()

        if capitalize_prepositions:
            formatted_words = [word.capitalize() for word in words]
        else:
            formatted_words = [word if word in prepositions else word.capitalize() for word in words]
        
        return " ".join(formatted_words)

    def get_state_acronym(self, state:str) -> str:
        acronyms = {
            "Acre": "AC",
            "Alagoas": "AL",
            "Amapá": "AP",
            "Amazonas": "AM",
            "Bahia": "BA",
            "Ceará": "CA",
            "Distrito Federal": "DF",
            "Espírito Santo": "ES",
            "Goiás": "GO",
            "Maranhão": "MA",
            "Mato Grosso": "MT",
            "Mato Grosso do Sul": "MS",
            "Minas Gerais": "MG",
            "Pará": "PA",
            "Paraíba": "PB",
            "Paraná": "PR",
            "Pernambuco": "PE",
            "Piauí": "PI",
            "Rio de Janeiro": "RJ",
            "Rio Grande do Norte": "RN",
            "Rio Grande do Sul": "RS",
            "Rondônia": "RO",
            "Roraima": "RR",
            "Santa Catarina": "SC",
            "São Paulo": "SP",
            "Sergipe": "SE",
            "Tocantins": "TO"
        }

        return acronyms[state]


if __name__ == "__main__":
    pass