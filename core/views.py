from django.http import HttpResponse
from .models import Session, Role, User, Story


def index(request):
    return HttpResponse('this is agile command central')
