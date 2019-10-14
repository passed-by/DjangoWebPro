import datetime
import json

from django_redis import get_redis_connection
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from contents.models import *
from user.models import Users


def merge():
    goodstype = FoodType.objects.all()
    activity = HotActivitys.objects.all()

    alltype = {}
    hotbrand = []
    ids = {}
    for child in goodstype:
        typelist = child.childtypename.split('#')
        brands = child.brand.split('#')
        childbrand = []
        for brand in brands:
            brandlist = brand.split(':')
            if brandlist[1] == '1':
                hotbrand.append(brandlist[0])
            childbrand.append(brandlist[0])
        activitys = activity.filter(activityid=child.activityid)
        ids[child.typename] = child.typeid
        activitys = [i.img for i in activitys]
        alltype[child.typename] = {'id': child.typeid, 'type': typelist, 'brand': childbrand, 'activities': activitys}

    # 计算购物车商品数量
    totalnum = 0
    islogin = ''
    redis_cart = get_redis_connection('cart')
    redis_session = get_redis_connection('session')
    userid = redis_session.get('userid')
    print(userid)
    if userid:
        userid = userid.decode()
        islogin = Users.objects.get(userid=int(userid)).username
        # print(islogin)
        redis_data = redis_cart.get(f'{userid}-cart')
        if redis_data:
            for i in json.loads(redis_data.decode()):
                totalnum += 1

    return [ids, alltype, hotbrand, totalnum, islogin]


# 首页
def index(request):

    wheels = MyShopWheel.objects.all()
    livetvs = LiveTV.objects.order_by('actiontime')
    today_perfer = PerferModel.objects.all()
    tvhots = TvHot.objects.all()
    news = ShopNews.objects.all()
    goods = Goods.objects.all()


    # 存放直播顺序
    livetvlist = []
    nowtime = datetime.datetime.now().strftime('%H:%M:%S')
    flag = False
    # 记录当前时间段的直播,以及下一个时间段的直播
    for i in livetvs:
        if flag:
            livetvlist.append(i)
            break
        if i.actiontime.split('~')[0] <= nowtime and i.actiontime.split('~')[1] >= nowtime:
            livetvlist.append(i)
            flag = True
    else:
        if len(livetvlist) != 2:
            livetvlist.append(livetvs.get(id=6))

    # print(livetvlist)
    #
    # print(livetvlist,livetvs.get(id=livetvlist[0].id),livetvs.get(id=livetvlist[0].id+1))


    # 商品分类
    classifications = merge()

    # tv热播
    tvhots = [tvhots[:5],tvhots[5:10],tvhots[10:15]]

    # 商品列表
    allgoods = {}
    n = 0
    change_type = request.GET.get('type','0')
    scroll_top = 420
    class_position = (0,0)
    for datakey, datavalue in classifications[1].items():
        n += 1
        titlepage = FoodType.objects.filter(typeid=datavalue["id"]).first().titlepage
        if change_type in datavalue["type"]:
            goodsone = goods.filter(categoryid=datavalue["id"]).filter(childcidname=change_type)[:6]
            scroll_top += scroll_top * n
            class_position = (datavalue["type"].index(change_type)+1, n)
        else:
            goodsone = goods.filter(categoryid=datavalue["id"]).order_by('-sales')[:6]
            # print(goodsone)
        allgoods[datakey] = {"id":[datavalue["id"],n],"titlepage": titlepage, "two_title": datavalue["type"], "goodsone": goodsone}
    # print(allgoods)

    content = {
        'ids': classifications[0],
        'alltype': classifications[1],
        'hotbrands': classifications[2],
        'totalnum': classifications[3],
        'islogin': classifications[4],
        'wheels':wheels[:5],
        'wheel2':wheels[5:6],
        'livetvs':{
            'onlivetv':livetvs.get(id=livetvlist[0].id),
            'nextlivetv':livetvs.get(id=livetvlist[1].id)
        },
        'todayperfer':today_perfer,
        'tvhots':tvhots,
        'news':news,
        'allgoods':allgoods,
        'hidden':scroll_top,
        'class_position':class_position
    }
    # print(allgoods)


    return render(request, 'index.html', content)


def showdetail(request, goodsid = 0):
    # 获取指定商品
    goods = Goods.objects.filter(goodsid=goodsid).first()
    if not goods:
        goods = TvHot.objects.filter(goodsid=goodsid).first()

    # 详情信息
    detailshow = goods.introduce.split('#')
    detaildict = {}
    for detail in detailshow:
        detaillist = detail.split('@')
        detaildict[detaillist[0]] = detaillist[1]
    # print(detaildict)

    # 获取分类部分
    classifications = merge()

    content = {
        'ids': classifications[0],
        'alltype': classifications[1],
        'hotbrands': classifications[2],
        'totalnum': classifications[3],
        'islogin': classifications[4],
        'goods':goods,
        'detaildict':detaildict
    }

    return render(request, 'details.html', content)