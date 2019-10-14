import random

import requests
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django_redis import get_redis_connection

# Create your views here.
from django.views import View

# 登陆界面
from comment.Middleware import loginmid
from user.models import Users

def login(request):

    if request.method == "GET":
        return render(request, 'login.html')

    if request.method == "POST":

        phone = request.POST.get('phone')
        verification = request.POST.get('password')
        remember = request.POST.get('remember')

        # 判断手机,验证码
        if not phone or not verification:
            return JsonResponse({'data':'bad'})

        if len(phone) > 6:
            user = Users.objects.filter(phone=phone).first()
        else:
            user = Users.objects.filter(userid=phone).first()

        if not user:
            return JsonResponse({'data':'user-null'})

        redis_cli = get_redis_connection()
        print(redis_cli.get(phone), type(redis_cli.get(phone)))

        if not redis_cli.get(phone):
            return JsonResponse({'data':'bad-verification'})

        if verification != redis_cli.get(phone).decode():
            return JsonResponse({'data': 'bad'})

        # 记住密码
        res = JsonResponse({'data':'ok'})
        if remember:
            res.set_cookie(str(user.userid),make_password(user.password))

        # 保存用户信息到redis
        redis_cli2 = get_redis_connection('session')
        idnum, password = user.userid, user.password
        redis_cli2.set('userid',str(idnum))

        return res



# 生成验证码
def verification(phone):
    num = random.randint(1000,9999)
    redis_cli = get_redis_connection()
    redis_cli.set(phone, num, 60)
    return num


# 发送短信
def check(request):
    phone = request.POST.get('phone')
    num = verification(phone)
    print(num,phone)

    data = {
        "sid": "8036ece41e07ea5340794286185f9214",
        "token": "8a9c9099eb825ea314bcb620f9fdbc6b",
        "appid": "cceff1236cee4e1e87b87186dc10ad27",
        "templateid": "493813",
        "param": num,
        "mobile": phone,
    }

    # data = {
    #     "sid": "787f46d6a9677722c20e2930b1ef10fe",
    #     "token": "124c792e011e8eede89be83f8c89344b",
    #     "appid": "2ab2575759c142ecb08e7b6ef354d9ed",
    #     "templateid": "503092",
    #     "param": num,
    #     "mobile": phone,
    # }

    # 用云之讯第三方发短信
    res = requests.post('https://open.ucpaas.com/ol/sms/sendsms', json=data)

    res = res.json()

    if res['code'] == '000000':
        print(res['code'] == '000000')
        return JsonResponse({'data':'send ok'})
    else:
        return JsonResponse({'res': 'send no'})


# 注册用户
class Register(View):

    def get(self, request):
        return render(request, 'registre.html')

    def post(self, request):
        phone = request.POST.get('phone')
        passnum = request.POST.get('passnum')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')

        user = Users.objects.filter(phone=phone).count()
        # print(user.get(phone=phone))
        # 判断用户是否存在
        if user:
            return JsonResponse({'data':'user-created'})

        # 判断验证码
        redis_cli = get_redis_connection()
        if not redis_cli.get(phone):
            return JsonResponse({'data':'passed-code'})

        if str(passnum) != redis_cli.get(phone).decode():
            return JsonResponse({'data': 'error-code'})

        # 检查密码
        if password1 != password2:
            return JsonResponse({'data': 'error-pwd'})

        # 生成用户编号
        userid = random.randint(10000,99999)
        if not email:
            email = ''

        # 新建用户
        # password2 = make_password(password2)
        user = Users.objects.create(
            username='FS-' + str(userid),
            userid=userid,
            phone=phone,
            password=password2,
            email=email,
        )

        if user:
            return JsonResponse({'data':'ok'})
        else:
            return JsonResponse({'data': 'error'})

@loginmid
def logout(request):
    print('logout...')
    redis_session = get_redis_connection('session')
    redis_session.set('userid','')
    return redirect(reverse('contents:index'))