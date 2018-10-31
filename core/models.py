from django.db import models
from django.contrib.auth.models import User


class Session(models.Model):
    name = models.CharField(max_length=30)
