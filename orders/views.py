from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import OrderDetail

def index(request):
	return HttpResponse("Hello, world. You're at the polls index.")

@login_required(login_url="login/")
def home(request):
	orders=OrderDetail.objects.all()
	return render(request,'home.html', {'orders': orders})