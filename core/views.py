from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model

from jira import JIRA, JIRAError

from .models import Session, Role, Story, User


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            jac = JIRA(
                'https://agilecommand.atlassian.net',
                basic_auth=(email, password)
            )
            jac_username = jac.myself().get('displayName')
            user = authenticate(request, username=email)
            if user is None:
                user = User(email=email, username=jac_username)
                user.save()
            login(request, user)
            return redirect('dashboard')
        except JIRAError as e:
            print('This is jira error: ' + str(e.status_code))
            return HttpResponse('Wrong login info')

    return render(request, 'login.html')


@login_required(login_url='/')
def dashboard(request):
    return HttpResponse('dashboard')
