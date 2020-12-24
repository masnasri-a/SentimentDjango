from django.shortcuts import render
from django.http import HttpResponse
import requests
import datetime

from .forms import Register
from .models import PostModel

def index(request):
    context = {"name":"nasri"}
    return render(request, 'index.html', context)

def login(request):
    if request.method=='GET':
        url = 'http://localhost:8899/get_account'
        response = requests.get(url)
        print(response.json())
        pass
    return render(request, 'login.html')

def register(request):
    hasil = Register(request.POST or None)
    if request.method == 'POST':
        datas = {"data":hasil.data}
        print(datas)
    
    return render(request, 'register.html')