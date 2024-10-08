from django.db import models
from django.contrib.auth.models import User

class SentimentAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional for authenticated users
    text = models.TextField()
    sentiment = models.CharField(max_length=20)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


# Create your models here.
