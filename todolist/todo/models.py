from django.db import models
from django.utils import timezone

# Create your models here.

def Todo():
    title = models.CharField()
    description = models.TextField()
    goal = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=timezone.now())
    completed = models.DateTimeField()
    important = models.BooleanField(default=False)
