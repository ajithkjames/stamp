from django.http import HttpResponse,Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import OrderDetail
from django.views.generic import View
from django.shortcuts import redirect
# from orders.models import User
# from django.contrib.auth import login

class Signup(View):
    template_name = "signup.html"
    def __init__(self, **kwargs):
        pass

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        try:
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            raw_password = request.POST.get("password")
            new_user = User.objects.create_user(email, first_name= first_name, last_name = last_name, email = email)
            new_user.set_password(raw_password)
            new_user.save()
            # login(self.request, new_user)
        except:
            pass
        return redirect('/')

@login_required(login_url="login/")
def home(request):
	orders=OrderDetail.objects.all()
	return render(request,'home.html', {'orders': orders})


def details(request,order_id):
	try:
		order=OrderDetail.objects.get(pk=order_id)
	except OrderDetail.DoesNotExist:
		raise Http404("No such order")
	return render(request,'order-details.html', {'order': order})

