from django.urls import path
from .views import HotmartProductsView, HotmartSalesView, ChatGPTView, index, CanvaWebhookView, CanvaDesignView

urlpatterns = [
    path('hotmart/products/', HotmartProductsView.as_view(), name='hotmart-products'),
    path('hotmart/sales/', HotmartSalesView.as_view(), name='hotmart-sales'),
    path('chatgpt/generate/', ChatGPTView.as_view(), name='chatgpt-generate'),
    path('canva/designs/', CanvaDesignView.as_view(), name='canva-designs'),
    path('canva/webhook/', CanvaWebhookView.as_view(), name='canva-webhook'),
    path('', index, name='index'),

]
