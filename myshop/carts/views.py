import json
import random
import string

from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django_redis import get_redis_connection

from comment.Middleware import loginmid
from contents.models import Goods, TvHot
from contents.views import merge


@loginmid
def cart(request):
    redis_cli_session = get_redis_connection('session')
    redis_cli_cart = get_redis_connection('cart')

    if request.method == "GET":
        onlineuserid = redis_cli_session.get('userid').decode()
        # print(onlineuserid)
        if not onlineuserid:
            return redirect(reverse('user:login'))

        # 根据登录用户取添加商品信息
        goods_cart = {}
        cart_data = redis_cli_cart.get(f'{onlineuserid}-cart')
        if not cart_data:
            cart_data = {}
        else:
            cart_data = json.loads(cart_data.decode())
        # print(cart_data)

        # 根据redis中的键查商品信息
            for data,value in cart_data.items():
                goods = Goods.objects.filter(goodsid=int(data)).first()
                if not goods:
                    goods = TvHot.objects.filter(goodsid=int(data)).first()

            # 组合数据
                goods_cart[goods.name] = {'id':goods.goodsid, 'img':goods.img, 'price':goods.price, 'inventory':goods.inventory, 'num':value['num'], 'selected':value['selected']}

        #生成secretkey,由组成随机字母,随机三位数,用户编号组成,
        # string.ascii_letters随机生成一个大/小写字母
        # 保存到redis
        action_key = random.choice(string.ascii_letters)
        end_key = str(random.randint(100,999))
        secretkey = action_key+end_key+str(onlineuserid)
        redis_key = get_redis_connection()   #默认的6号库
        redis_key.set(f"{onlineuserid}-key",secretkey)

        classifications = merge()

        content = {
            'ids': classifications[0],
            'alltype': classifications[1],
            'hotbrands': classifications[2],
            'totalnum': classifications[3],
            'islogin': classifications[4],
            'goodscarts':goods_cart,
            'secretkey':secretkey
        }

        return render(request, 'cart.html', content)

    elif request.method == "POST":
        gid = request.POST.get('gid')
        number = request.POST.get('number')
        try:
            number = int(number)
        except:
            return JsonResponse({'data':'num-bad'})


        # 存数据到redis
        userid = redis_cli_session.get('userid').decode()
        goodsdict = redis_cli_cart.get(f'{userid}-cart')
        selected = 'true'

        if not goodsdict:
            goodsdict = {gid: {"num": number, "selected": selected}}
        else:
            goodsdict = json.loads(goodsdict)
            if goodsdict.get(gid):
                goodsdict[gid] = {"num": str(int(goodsdict[gid]["num"]) + number), "selected": selected}
            else:
                goodsdict[gid] = {"num": number, "selected": selected}


        redis_cli_cart.set(f'{userid}-cart', json.dumps(goodsdict))


        return JsonResponse({'data':'add-ok','nums':str(number)})


@loginmid
def updateselected(request):
    redis_cli_cart = get_redis_connection('cart')
    redis_cli_session = get_redis_connection('session')

    # 获取参数
    userid = redis_cli_session.get('userid').decode()
    num = request.POST.get('num')
    gid = request.POST.get('gid')
    selected = request.POST.get('selected')

    # 获取所有商品信息
    cart_data = redis_cli_cart.get(f'{userid}-cart').decode()
    cart_data = json.loads(cart_data)

    # 改变cookie中的商品数量
    cart_data[gid]["num"] = num
    cart_data[gid]["selected"] = selected

    # 删除数量0的商品
    if num == '0':
        del cart_data[gid]

    # 重新添加商品
    redis_cli_cart.set(f'{userid}-cart', json.dumps(cart_data))

    return JsonResponse({'res': 'checked-ok'})


# 清空购物车
@loginmid
def deleteall(request):
    redis_cart = get_redis_connection('cart')
    redis_session = get_redis_connection('session')
    redis_key = get_redis_connection()
    secretkey = request.POST.get('secretkey')
    print(secretkey)

    # 判断secretkey
    onlineuserid = redis_session.get('userid').decode()
    redis_secretkey = redis_key.get(f"{onlineuserid}-key").decode()
    if redis_secretkey != secretkey:
        return JsonResponse({'data':'bad-key'})

    # 清空购物车数据
    redis_cart.set(f"{onlineuserid}-cart",json.dumps({}))
    return JsonResponse({'data':'ok'})