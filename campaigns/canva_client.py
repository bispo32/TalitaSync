import requests

CANVA_API_BASE_URL = "https://api.canva.com/v1"


def get_canva_access_token(client_id, client_secret):
    url = f"{CANVA_API_BASE_URL}/oauth2/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()['access_token']


def create_design(access_token, template_id, design_data):
    url = f"{CANVA_API_BASE_URL}/templates/{template_id}/designs"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=design_data, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()
