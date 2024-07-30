from django.contrib import admin
from .models import Campaign, ChatGPTRequest, ChatGPTResponse


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'budget', 'start_date', 'end_date', 'created_at')
    search_fields = ('name',)
    list_filter = ('start_date', 'end_date')


@admin.register(ChatGPTRequest)
class ChatGPTRequestAdmin(admin.ModelAdmin):
    list_display = ('prompt', 'created_at')
    search_fields = ('prompt',)
    list_filter = ('created_at',)


@admin.register(ChatGPTResponse)
class ChatGPTResponseAdmin(admin.ModelAdmin):
    list_display = ('request', 'response_text', 'created_at')
    search_fields = ('response_text',)
    list_filter = ('created_at',)
