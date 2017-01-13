from django.http import HttpResponse, Http404
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import OrderDetail
from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import OrderDetailForm
from orders.models import User
from django.contrib.auth import login

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
			login(self.request, new_user)
		except:
			return redirect('/')
		return redirect('/')

# @login_required(login_url="login/")
class HomeView(LoginRequiredMixin, generic.ListView):
	template_name= 'home.html'

	def get_queryset(self):
		return OrderDetail.objects.filter(user=self.request.user)

class DetailsView(LoginRequiredMixin, generic.DetailView):
	model = OrderDetail

	def get_object(self, *args, **kwargs):
		obj = super(DetailsView, self).get_object(*args, **kwargs)
		if not obj.user == self.request.user:
			raise Http404 # maybe you'll need to write a middleware to catch 403's same way
		return obj
	template_name= 'order-details.html'

def create_order(request):
	if not request.user.is_authenticated():
		return render(request, '/')
	else:
		form = OrderDetailForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			orderdetail = form.save(commit=False)
			orderdetail.user = request.user
			orderdetail.save()
			return redirect('/')
		context = {
			"form": form,
		}
		return render(request, 'createorder.html', context)



class update_order(LoginRequiredMixin, UpdateView):
	model = OrderDetail
	fields = ['user','stamp_type','size','font','color','allignment','rate','quantity','spcl_request','advance','delivery_date',]





# def home(request):
# 	orders=OrderDetail.objects.all()
# 	return render(request,'home.html', {'orders': orders})


# def details(request,order_id):
# 	order=get_object_or_404(OrderDetail, pk=order_id)
# 	return render(request,'order-details.html', {'order': order})

