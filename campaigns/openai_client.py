import openai
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Definir a chave da API do OpenAI
openai.api_key = os.getenv('sk-proj-JaTIlbV4K5UXaWBKmjx5T3BlbkFJTL5UNg37fAgfgaEPAl0w')


def generate_text(prompt):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=150,
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            print(f"Error generating text: {e}")
            raise e
