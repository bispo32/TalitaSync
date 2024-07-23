import requests


def get_hotmart_access_token(client_id, client_secret):
    url = "https://api-sec-vlc.hotmart.com/security/oauth/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception("Failed to obtain access token")


def get_hotmart_products(access_token):
    url = "https://api-sec-vlc.hotmart.com/products/v2"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch products")


def get_hotmart_sales(access_token):
    url = "https://api-sec-vlc.hotmart.com/reports/v1/sales"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch sales")
