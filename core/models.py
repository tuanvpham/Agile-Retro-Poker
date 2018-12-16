from django.db import models
from django.contrib.auth.models import AbstractUser

AbstractUser._meta.get_field('email')._unique = True
AbstractUser._meta.get_field('username')._unique = False


class Session(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Role(models.Model):
    ROLES = (
        ('H', 'Host'),
        ('A', 'Attendee'),
    )
    title = models.CharField(max_length=30, choices=ROLES, null=True)

    def __str__(self):
        return self.title


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Story(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True, blank=True)
    story_points = models.IntegerField()
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
