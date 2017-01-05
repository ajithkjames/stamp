from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views
from orders.forms import LoginForm
from orders.views import Signup

urlpatterns = [
 	url(r'^', include('orders.urls')),
    url(r'^orders/', include('orders.urls')),
    url(r'^login/$', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm,'redirect_authenticated_user': True},name='login'), 
    # url(r'^login/', auth_views.login, name='login',
    #     kwargs={'redirect_authenticated_user': True}),
    url(r'^admin/', admin.site.urls),
    url(r'^logout/$', views.logout, {'next_page': '/login'}),
    url(r'^signup/$', Signup.as_view()),
]