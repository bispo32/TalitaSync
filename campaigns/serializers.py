from rest_framework import serializers
from .models import Campaign, ChatGPTRequest, ChatGPTResponse


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'


class ChatGPTRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGPTRequest
        fields = '__all__'


class ChatGPTResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGPTResponse
        fields = '__all__'


class ChatGPTRequestSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=1000)


class ChatGPTResponseSerializer(serializers.Serializer):
    text = serializers.CharField()