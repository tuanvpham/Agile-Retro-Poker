from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class Session(models.Model):
    name = models.CharField(max_length=30)


class Role(models.Model):
    name = models.CharField(max_length=30)


class User(AbstractUser):
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)


class Story(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    story_points = models.IntegerField()
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
