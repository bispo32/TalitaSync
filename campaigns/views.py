from django.shortcuts import render
from rest_framework import status, generics
from rest_framework import viewsets
from .models import Campaign, ChatGPTRequest, ChatGPTResponse
from .serializers import CampaignSerializer, ChatGPTRequestSerializer, ChatGPTResponseSerializer
from .openai_client import generate_text
from rest_framework.views import APIView
from rest_framework.response import Response
from .hotmart import get_hotmart_access_token, get_hotmart_products, get_hotmart_sales
import requests
from .forms import CampaignForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView, CreateView
import openai


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
    response = requests.post(HOTMART_TOKEN_URL, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        return None


class HotmartProductsView(ListView):
    template_name = 'campaigns/hotmart_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        access_token = get_hotmart_access_token()
        if access_token:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.get(f"{HOTMART_API_BASE_URL}/v2/products", headers=headers)
            if response.status_code == 200:
                return response.json()['items']
        return []


def index(request):
    return render(request, 'campaigns/index.html')


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer


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


class CampaignListView(ListView):
    model = Campaign
    template_name = 'campaigns/index.html'
    context_object_name = 'campaigns'


class CampaignCreateView(CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'campaigns/create_campaign.html'
    success_url = reverse_lazy('index')


def generate_text(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        openai.api_key = 'your_openai_api_key'
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        text = response.choices[0].text.strip()
        return JsonResponse({'text': text})
    return JsonResponse({'error': 'Invalid request'}, status=400)