from django.shortcuts import redirect
from django.urls import reverse
from django_redis import get_redis_connection

def loginmid(func):
    def inner(*args,**kwargs):
        redis_session = get_redis_connection('session')
        print(redis_session.get('userid'))
        if not redis_session.get('userid'):
            return redirect(reverse('user:login'))
        return func(*args,**kwargs)
    return inner