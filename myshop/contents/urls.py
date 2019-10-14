from django.conf.urls import url

from contents import views

urlpatterns = [
    url('^index/$', views.index, name='index'),
    url('^detail/(\d+)/$', views.showdetail, name='detail'),
]