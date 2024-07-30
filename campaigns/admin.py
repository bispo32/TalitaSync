from django.contrib import admin
from .models import Campaign, ChatGPTRequest, ChatGPTResponse, CampaignPrompt


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


@admin.register(CampaignPrompt)
class CampaignPromptAdmin(admin.ModelAdmin):
    list_display = ('prompt', 'created_at')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # Se é um novo objeto
            ad_text = generate_campaign_text(obj.prompt)
            # Chame a função para criar a campanha no Google Ads (quando implementada)