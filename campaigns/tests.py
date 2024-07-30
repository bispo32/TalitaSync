from django.test import TestCase
from unittest.mock import patch
from .openai_client import generate_campaign_text
from .google_ads import create_google_ads_campaign
from .models import CampaignPrompt


class ChatGPTTests(TestCase):
    def test_generate_campaign_text(self):
        prompt = "Create an ad for a new product"
        with patch('openai.Completion.create') as mock_create:
            mock_create.return_value.choices = [type('obj', (object,), {'text': 'Ad text'})]
            ad_text = generate_campaign_text(prompt)
            self.assertEqual(ad_text, 'Ad text')


class GoogleAdsTests(TestCase):
    def test_create_google_ads_campaign(self):
        client_customer_id = 'test-customer-id'
        campaign_name = 'Test Campaign'
        budget_amount = 100
        ad_text = 'Ad text'

        with patch('google.ads.google_ads.client.GoogleAdsClient.load_from_storage') as mock_load, \
                patch('google.ads.google_ads.client.GoogleAdsClient.get_service') as mock_service, \
                patch('google.ads.google_ads.client.GoogleAdsClient.get_type') as mock_type:
            mock_client = mock_load.return_value
            mock_service.return_value = mock_type.return_value

            create_google_ads_campaign(client_customer_id, campaign_name, budget_amount, ad_text)

            mock_load.assert_called_once()
            mock_service.assert_called()
            mock_type.assert_called()


class CampaignPromptTests(TestCase):
    def test_create_campaign_prompt(self):
        prompt_text = "Create an ad for a new product"
        prompt = CampaignPrompt.objects.create(prompt=prompt_text)
        self.assertEqual(prompt.prompt, prompt_text)
        self.assertIsNotNone(prompt.created_at)
