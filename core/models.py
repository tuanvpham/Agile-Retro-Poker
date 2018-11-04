from django.db import models
from django.contrib.auth.models import AbstractUser


class Session(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return '%s with %s role and %s session' % (
            self.username,
            self.role,
            self.session
        )


class Story(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    story_points = models.IntegerField()
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
