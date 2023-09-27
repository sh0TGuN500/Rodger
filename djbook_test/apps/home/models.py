from django.db import models
from django.contrib.auth.models import User


class GuestData(models.Model):
    user = models.CharField(max_length=100)
    device = models.TextField()
    address = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=False)
