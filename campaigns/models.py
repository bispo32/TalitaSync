from django.db import models


class Campaign(models.Model):
    name = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ChatGPTRequest(models.Model):
    prompt = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request at {self.created_at}: {self.prompt[:50]}"


class ChatGPTResponse(models.Model):
    request = models.ForeignKey(ChatGPTRequest, on_delete=models.CASCADE, related_name='responses')
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to Request {self.request.id}: {self.response_text[:50]}"
