from django.conf.urls import url

from user import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^verification/$', views.check, name='verification'),
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^logout/$', views.logout, name='logout'),
]