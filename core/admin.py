from django.contrib import admin
from .models import Session, Role, User, Story

models = Session, Role, User, Story
admin.site.register(models)
