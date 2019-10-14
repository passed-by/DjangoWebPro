from django.conf.urls import url

from carts import views

urlpatterns = [
    url(r'^cart/$', views.cart, name='index'),

    url(r'^update/$', views.updateselected, name='update'),

    url(r'^deleteall/$', views.deleteall, name='deleteall'),

]