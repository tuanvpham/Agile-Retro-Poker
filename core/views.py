from django.shortcuts import render
from django.http import HttpResponse

import mysql.connector

# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")

def connect_db():
	cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='dacc_db')
