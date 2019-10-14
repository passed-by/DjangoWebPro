from django.conf.urls import url

from orders import views

urlpatterns = [
    url(r'^pay/(\d+)/$', views.pay, name='pay'),

    url(r'^orders/$', views.orders, name='index'),

    url(r'^payback/$', views.payback, name='payback'),

    url(r'^orderdetail/(\d+)/$', views.orderdetail, name='orderdetail'),

    url(r'^buy_now/$', views.buy_now, name='buy_now'),

]