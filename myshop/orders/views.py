import datetime
import json
import os

from alipay import AliPay
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django_redis import get_redis_connection

# Create your views here.
from comment.Middleware import loginmid
from contents.models import Goods, TvHot
from contents.views import merge
from myshop import settings
from orders.models import Order, OrderDetail


@loginmid
def orders(request):
    if request.method == "GET":
        orders = Order.objects.filter(total_count__gt=0).order_by('-order_code')

        # 未支付的订单字典
        orderdict = {}
        i = 0
        for data in orders:
            i += 1
            order_time = data.order_code[:4] + "年 " + data.order_code[4:6] + "月 " + \
                         data.order_code[6:8] + "日 " + data.order_code[8:10] + "时 " + data.order_code[10:12] + "分 "
            status = ""
            if data.status == 1:
                status = "未支付"
            elif data.status == 2:
                status = "未发货"
            elif data.status == 3:
                status = "正在派送"
            orderdict[data.order_code] = {
                "id":i,
                "order_time":order_time,
                "num":data.total_count,
                "totalmonery":data.total_amount,
                "status":status
            }

        classifications = merge()

        content = {
            "orders":orderdict,
            'islogin': classifications[4],
        }
        print(orderdict)
        return render(request, 'order.html', content)

    elif request.method == "POST":
        redis_cli_cart = get_redis_connection('cart')
        redis_cli_session = get_redis_connection('session')

        userid = redis_cli_session.get('userid').decode()
        if not userid:
            return JsonResponse({'data':'null-user'})

        # 已经登陆后才获取订单数据
        # 从redis中获取订单
        redis_data = redis_cli_cart.get(f'{userid}-cart')
        print(redis_data)
        if not redis_data:
            return JsonResponse({'data':'null-cart'})
        redis_data = json.loads(redis_data)

        # 选出选中的商品
        cart_dict = {}
        for goodsid, data in redis_data.items():

            if data.get('selected') == 'true':
                cart_dict[int(goodsid)] = int(data['num'])

        if sum(cart_dict.values()) == 0:
            return JsonResponse({'data':'zero-num'})

        # 开启事务
        with transaction.atomic():

            # 添加事务保存点
            save_id = transaction.savepoint()

            # 订单编号
            order_code = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(userid)

            # 生成订单
            order = Order.objects.create(
                userid=userid,
                order_code=order_code,
                total_count=sum(cart_dict.values()),
                total_amount=0,
                status=1
            )

            # print(cart_dict)   # {496: 2, 495: 2}
            totalprice = 0
            for gid, gnum in cart_dict.items():
                while True:
                    goods = Goods.objects.filter(goodsid=gid).first()
                    if not goods:
                        goods = TvHot.objects.filter(goodsid=gid).first()

                    # 判断购买商品数量是否合理
                    if gnum > goods.inventory:
                        # 回滚事务
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({'data':'not-have','goods':gid})

                    res = Goods.objects.filter(goodsid=goods.goodsid, inventory=goods.inventory).update(
                        inventory=goods.inventory - gnum,
                        sales=goods.sales + gnum
                    )
                    if not res:
                        res = TvHot.objects.filter(goodsid=goods.goodsid, inventory=goods.inventory).update(
                            inventory=goods.inventory - gnum,
                            sales=goods.sales + gnum
                        )

                    if not res:
                        continue  # 如果库存够，并发执行失败后，重新执行

                    # 生成子订单
                    OrderDetail.objects.create(
                        order_code=order_code,
                        goods_id=gid,
                        counts=gnum,
                        price=goods.price,
                    )

                    totalprice += goods.price * gnum

                    # 删除redis中已经下单的商品信息
                    del redis_data[str(gid)]
                    break

            order.total_amount = totalprice
            order.save()

            redis_cli_cart.set(f'{userid}-cart', json.dumps(redis_data))

            # 提交事务
            transaction.savepoint_commit(save_id)
        print(redis_data)

        return JsonResponse({'data':'ok'})



# 支付宝支付函数
@loginmid
def pay(request, order_code):
    alipay = AliPay(
        appid='2016092700609211',
        app_notify_url=None,  # 默认回调url
        app_private_key_path=os.path.join(settings.BASE_DIR, "alipay/app_private_key.pem"),
        alipay_public_key_path=os.path.join(settings.BASE_DIR, "alipay/alipay_public_key.pem"),
        sign_type="RSA2",
        debug=True
    )

    order = Order.objects.get(order_code=order_code)

    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_code,
        total_amount=float(order.total_amount),
        subject='商品支付信息',
        return_url='http://127.0.0.1:8000/payback/',
    )

    alipay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
    return redirect(alipay_url)


# 支付宝回调接口
def payback(request):

    query_dict = request.GET
    data = query_dict.dict()

    # 获取并从请求参数中剔除signature
    signature = data.pop('sign')

    # 创建支付宝支付对象
    alipay = AliPay(
        appid='2016092700609211',
        app_notify_url=None,  # 默认回调url
        app_private_key_path=os.path.join(settings.BASE_DIR, "alipay/app_private_key.pem"),
        alipay_public_key_path=os.path.join(settings.BASE_DIR, "alipay/alipay_public_key.pem"),
        sign_type="RSA2",
        debug=True
    )
    # 校验这个重定向是否是alipay重定向过来的
    success = alipay.verify(data, signature)

    if success:
        # 验证成功
        # 改变订单状态
        order_code = data['out_trade_no']
        print(order_code)
        Order.objects.filter(order_code=order_code).update(status=3)
        return redirect(reverse('orders:index'))
    else:
      	# 验证失败
        print('no')
        return HttpResponse('no')


@loginmid
def orderdetail(request, orderid):
    order = OrderDetail.objects.filter(order_code=orderid)

    ordersdetail = {}
    i = 0
    for data in order:
        i += 1
        goods = Goods.objects.filter(goodsid=data.goods_id).first()
        if not goods:
            goods = TvHot.objects.filter(goodsid=data.goods_id).first()
        orders = Order.objects.filter(order_code=data.order_code).first()
        status = "未支付"
        if orders.status == 1:
            pass
        elif orders.status == 2:
            status = "未发货"
        elif orders.status == 3:
            status = "派送中"
        ordersdetail[goods.goodsid] = {
            "id":i,
            "code":data.order_code,
            "gname":goods.name,
            "gnum":data.counts,
            "price":goods.price,
            "totalprice":float(goods.price * data.counts),
            "status":status
        }

    classifications = merge()

    content = {
        'ordersdetail':ordersdetail,
        'islogin': classifications[4],
    }

    return render(request, 'orderdetail.html', content)


@loginmid
def buy_now(request):
    if request.method == "POST":
        redis_cli_session = get_redis_connection('session')
        userid = redis_cli_session.get('userid').decode()


        gid = request.POST.get('gid')
        number = request.POST.get('number')
        number = int(number)

        with transaction.atomic():
            # 添加事务保存点
            save_id = transaction.savepoint()

            # 订单编号
            order_code = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(userid)

            # 生成订单
            order = Order.objects.create(
                userid=userid,
                order_code=order_code,
                total_count=number,
                total_amount=0,
                status=1
            )

            totalprice = 0
            while True:
                goods = Goods.objects.filter(goodsid=gid).first()
                if not goods:
                    goods = TvHot.objects.filter(goodsid=gid).first()
                print(number,goods.inventory)

                # 判断购买商品数量是否合理
                if number > goods.inventory:
                    # 回滚事务
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'data': 'not-have'})

                res = Goods.objects.filter(goodsid=goods.goodsid, inventory=goods.inventory).update(
                    inventory=goods.inventory - number,
                    sales=goods.sales + number
                )
                if not res:
                    res = TvHot.objects.filter(goodsid=goods.goodsid, inventory=goods.inventory).update(
                        inventory=goods.inventory - number,
                        sales=goods.sales + number
                    )

                if not res:
                    continue  # 如果库存够，并发执行失败后，重新执行

                # 生成子订单
                OrderDetail.objects.create(
                    order_code=order_code,
                    goods_id=gid,
                    counts=number,
                    price=goods.price,
                )

                totalprice += goods.price * number
                break

            order.total_amount = totalprice
            order.save()
            transaction.savepoint_commit(save_id)

        return JsonResponse({'data':'ok'})
