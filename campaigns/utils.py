import jwt
from jwt.algorithms import get_default_algorithms
from .canva_keys import fetch_canva_keys
import openai

# Certifique-se de definir sua chave de API do OpenAI
openai.api_key = 'sk-proj-JaTIlbV4K5UXaWBKmjx5T3BlbkFJTL5UNg37fAgfgaEPAl0w'


def verify_canva_webhook(signature, payload):
    keys = fetch_canva_keys()
    for key in keys:
        public_key = jwt.algorithms.ECAlgorithm.from_jwk(key)
        try:
            decoded_signature = jwt.decode(signature, public_key, algorithms=["EdDSA"], options={"verify_aud": False})
            return decoded_signature
        except jwt.InvalidTokenError:
            continue
    raise ValueError("Invalid signature")


def generate_text(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()
