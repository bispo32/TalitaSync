from django.shortcuts import render
from rest_framework import status, generics
from rest_framework import viewsets
from .canva_client import get_canva_access_token, create_design
from .models import Campaign, ChatGPTRequest, ChatGPTResponse
from .serializers import CampaignSerializer, ChatGPTRequestSerializer, ChatGPTResponseSerializer
from .openai_client import generate_text
from rest_framework.views import APIView
from rest_framework.response import Response
from .hotmart import get_hotmart_access_token, get_hotmart_products, get_hotmart_sales
from .utils import verify_canva_webhook

import requests

HOTMART_CLIENT_ID = '0cc8276b-0793-4ee5-800b-1a2aa2421efe'
HOTMART_CLIENT_SECRET = '798ea082-aa6b-4196-b4b0-b1599888a2e6'
HOTMART_TOKEN_URL = 'https://api-sec-vlc.hotmart.com/security/oauth/token'
HOTMART_API_BASE_URL = "https://api.hotmart.com"


def get_hotmart_access_token():
    data = {
        'grant_type': 'client_credentials',
        'client_id': HOTMART_CLIENT_ID,
        'client_secret': HOTMART_CLIENT_SECRET
    }
    try:
        response = requests.post(HOTMART_TOKEN_URL, data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Content: {response.content.decode('utf-8')}")  # Linha de debug

        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return None


class HotmartProductsView(APIView):
    def get(self, request):
        access_token = get_hotmart_access_token()
        if access_token:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.get(f"{HOTMART_API_BASE_URL}/v2/products", headers=headers)
            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to fetch products from Hotmart"}, status=response.status_code)
        else:
            return Response({"error": "Failed to obtain access token"}, status=status.HTTP_401_UNAUTHORIZED)


class HotmartSalesView(APIView):
    def get(self, request):
        access_token = get_hotmart_access_token()
        if access_token:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.get(f"{HOTMART_API_BASE_URL}/v2/sales", headers=headers)
            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to fetch sales from Hotmart"}, status=response.status_code)
        else:
            return Response({"error": "Failed to obtain access token"}, status=status.HTTP_401_UNAUTHORIZED)


class ChatGPTView(APIView):
    def post(self, request):
        try:
            api_key = "sk-proj-JaTIlbV4K5UXaWBKmjx5T3BlbkFJTL5UNg37fAgfgaEPAl0w"
            prompt = request.data.get('prompt')
            text = generate_text(prompt, api_key)
            return Response({"text": text}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChatGPTView(APIView):
    def post(self, request):
        serializer = ChatGPTRequestSerializer(data=request.data)
        if serializer.is_valid():
            prompt = serializer.validated_data.get('prompt')
            try:
                text = generate_text(prompt)
                response_serializer = ChatGPTResponseSerializer({"text": text})
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatGPTRequestListView(generics.ListAPIView):
    queryset = ChatGPTRequest.objects.all()
    serializer_class = ChatGPTRequestSerializer


class ChatGPTResponseListView(generics.ListAPIView):
    queryset = ChatGPTResponse.objects.all()
    serializer_class = ChatGPTResponseSerializer


class CanvaWebhookView(APIView):
    def post(self, request):
        signature = request.headers.get('X-Canva-Signature')
        payload = request.body
        if not signature:
            return Response({"error": "Signature header is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            verify_canva_webhook(signature, payload)
            # Processar o webhook aqui
            return Response({"message": "Webhook received and verified"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CanvaDesignView(APIView):
    def post(self, request):
        try:
            client_id = 'OC-AZCypyBx0xO7'
            client_secret = 'cnvcamCXC4nxhWIQSYtbJgaR2R1OCdMLiWOi8P2lpn4vsC0kaa8a5db5'
            access_token = get_canva_access_token(client_id, client_secret)
            template_id = request.data.get('template_id')
            design_data = request.data.get('design_data')
            design = create_design(access_token, template_id, design_data)
            return Response(design, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def index(request):
    return render(request, 'campaigns/index.html')


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

