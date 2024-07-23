import requests

CANVA_KEYS_URL = "https://api.canva.com/rest/v1/connect/keys"


def fetch_canva_keys():
    response = requests.get(CANVA_KEYS_URL)
    response.raise_for_status()  # Levanta uma exceção para erros HTTP
    return response.json()['keys']
