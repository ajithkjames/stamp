from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^(?P<pk>[0-9]+)/$',views.DetailsView.as_view(), name='detail'),
    url(r'^create-order/$', views.create_order, name='create_order'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.update_order.as_view(), name='update_order'),
]