from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from orders.forms import LoginForm
from orders.views import Signup,Profile_view,edit_profile,create_profile,AdminHomeView,search,HelloPDFView

urlpatterns = [
 	url(r'^$', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm,'redirect_authenticated_user': True},name='login'),
    url(r'^orders/', include('orders.urls')),
    url(r'^login/$', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm,'redirect_authenticated_user': True},name='login'), 
    # url(r'^login/', auth_views.login, name='login',
    #     kwargs={'redirect_authenticated_user': True}),
    url(r'^admin/', admin.site.urls),
    url(r'^logout/$', views.logout, {'next_page': '/login'}),
    url(r'^signup/$', Signup.as_view()),
    url(r'^oauth/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^create-profile/$', create_profile, name='create-profile'),
    url(r'^profile/$', Profile_view, name='profile'),
    url(r'^edit-profile/(?P<pk>[0-9]+)/$', edit_profile.as_view(), name='edit-profile'),
    url(r'^admin-home/$', AdminHomeView.as_view(), name='admin-home'),
    url(r'^search/$', search, name='search'),
    url(r"^pdf$", HelloPDFView.as_view()),
]

admin.site.index_template = 'customadmin.html'
admin.autodiscover()


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)