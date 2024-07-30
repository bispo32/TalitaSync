import aiohttp
import asyncio
import jwt
from jwt.algorithms import get_default_algorithms
import openai

# Certifique-se de definir sua chave de API do OpenAI
openai.api_key = 'sk-proj-JaTIlbV4K5UXaWBKmjx5T3BlbkFJTL5UNg37fAgfgaEPAl0w'
GOOGLE_ADS_API_URL = 'AIzaSyBQTS8wNB_mvDd9hAaFE4N8QdE0pF233T4'
HOTMART_CLIENT_ID = '0cc8276b-0793-4ee5-800b-1a2aa2421efe'
HOTMART_CLIENT_SECRET = '798ea082-aa6b-4196-b4b0-b1599888a2e6'
HOTMART_TOKEN_URL = 'https://api-sec-vlc.hotmart.com/security/oauth/token'
HOTMART_API_BASE_URL = "https://api.hotmart.com"


def generate_text(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()


async def get_hotmart_access_token(session):
    data = {
        'grant_type': 'client_credentials',
        'client_id': HOTMART_CLIENT_ID,
        'client_secret': HOTMART_CLIENT_SECRET
    }
    async with session.post(HOTMART_TOKEN_URL, data=data) as response:
        if response.status == 200:
            json_response = await response.json()
            return json_response.get('access_token')
        else:
            print("Failed to obtain access token")
            return None


async def get_hotmart_products(session, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    async with session.get(f"{HOTMART_API_BASE_URL}/v2/products", headers=headers) as response:
        if response.status == 200:
            json_response = await response.json()
            return json_response['items']
        else:
            print("Failed to fetch products")
            return []


async def generate_text(session, prompt):
    headers = {
        'Authorization': f'Bearer {openai.api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'prompt': prompt,
        'max_tokens': 150
    }
    async with session.post('https://api.openai.com/v1/engines/davinci/completions', headers=headers, json=data) as response:
        if response.status == 200:
            json_response = await response.json()
            return json_response['choices'][0]['text'].strip()
        else:
            print("Failed to generate text")
            return ""


async def create_google_ads_campaign(session, campaign_data):
    async with session.post(GOOGLE_ADS_API_URL, json=campaign_data) as response:
        if response.status == 200:
            json_response = await response.json()
            return json_response
        else:
            print("Failed to create campaign")
            return None
