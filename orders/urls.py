from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<order_id>[0-9]+)/$',views.details, name='detail'),
]