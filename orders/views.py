from django.http import HttpResponse, Http404
from django.shortcuts import render,get_object_or_404,render_to_response
from django.contrib.auth.decorators import login_required
from .models import OrderDetail,Profile
from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import OrderDetailForm,ProfileForm
from orders.models import User
from django.contrib.auth import login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re
from django.db.models import Q
from django.template import RequestContext

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

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
class AdminHomeView(LoginRequiredMixin,View):
	template_name= 'admin.html'

	def get(self, request):
		order=OrderDetail.objects.all().order_by('-created_at')
		page = request.GET.get('page', 1)
		paginator = Paginator(order, 10)
		try:
			orders = paginator.page(page)
		except PageNotAnInteger:
		    orders = paginator.page(1)
		except EmptyPage:
		    orders = paginator.page(paginator.num_pages)
		return render(request, self.template_name, {'order': orders})
		# context = {
		# 	"order": order,
		# }
		# if request.user.is_superuser:
		# 	return render(request, self.template_name, context)
		# else:
		# 	return redirect('/')
	
		
# @login_required(login_url="login/")
class HomeView(LoginRequiredMixin, generic.ListView):
	template_name= 'home.html'
	
	def get_queryset(self):
		return OrderDetail.objects.filter(user=self.request.user).order_by('-created_at')

def Profile_view(request):
	if not request.user.is_authenticated():
		return render(request, '/')
	else:
		if request.user.is_superuser:
			return redirect('/admin-home')
		else:
			if hasattr(request.user, 'profile'):
				profile=Profile.objects.get(user=request.user)
				context = {
					"profile": profile,
				}
				return render(request, 'profile.html', context)
			else:
				return redirect('/create-profile')
class DetailsView(LoginRequiredMixin, generic.DetailView):
	model = OrderDetail

	def get_object(self, *args, **kwargs):
		obj = super(DetailsView, self).get_object(*args, **kwargs)
		if not obj.user == self.request.user:
			if self.request.user.is_superuser:
				return obj
			else:
				raise Http404 # maybe you'll need to write a middleware to catch 403's same way
		return obj
	template_name= 'order-details.html'

def create_order(request):
	if not request.user.is_authenticated():
		return render(request, '/')
	else:
		if hasattr(request.user, 'profile'):
			form = OrderDetailForm(request.POST or None, request.FILES or None)
			if form.is_valid():
				orderdetail = form.save(commit=False)
				orderdetail.user = request.user
				orderdetail.save()
				return redirect('/orders')
			context = {
				"form": form,
			}
			return render(request, 'createorder.html', context)
		else:
			return redirect('/create-profile')

def create_profile(request):
	if not request.user.is_authenticated():
		return render(request, '/')
	else:
		form = ProfileForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			profile = form.save(commit=False)
			profile.user = request.user
			profile.avatar = request.FILES['avatar']
			file_type = profile.avatar.url.split('.')[-1]
			file_type = file_type.lower()
			if file_type not in IMAGE_FILE_TYPES:
				context ={
				    'profile': profile,
				    'form': form,
				    'error_message': 'Image file must be PNG, JPG, or JPEG',
				}
				return render(request, 'createprofile.html', context)
			profile.save()
			return redirect('/profile')
		context = {
			"form": form,
		}
		return render(request, 'createprofile.html', context)

class update_order(LoginRequiredMixin, UpdateView):
	model = OrderDetail
	fields = ['user','stamp_type','size','font','color','allignment','rate','quantity','spcl_request','advance','delivery_date',]

class edit_profile(LoginRequiredMixin, UpdateView):
	model = Profile
	fields = ['avatar','company','designation','phone','address']


# def home(request):
# 	orders=OrderDetail.objects.all()
# 	return render(request,'home.html', {'orders': orders})


# def details(request,order_id):
# 	order=get_object_or_404(OrderDetail, pk=order_id)
# 	return render(request,'order-details.html', {'order': order})



def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        entry_query = get_query(query_string, [ 'user__first_name','user__email','stamp_type'])
        
        found_entries = OrderDetail.objects.filter(entry_query)

    return render(request,'search_results.html',
                          { 'query_string': query_string, 'found_entries': found_entries })