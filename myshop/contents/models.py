from django.db import models

# Create your models here.
# 轮播图模型
class MyShopWheel(models.Model):
    img = models.CharField(max_length=255, verbose_name="图片信息")
    name = models.CharField(max_length=100, verbose_name="文字信息")

    class Meta:
        db_table = 'myshop_wheel'


#  正在直播模型
class LiveTV(models.Model):
    img = models.CharField(max_length=255, verbose_name="图片信息")
    actiontime = models.CharField(max_length=100, verbose_name="直播时间")
    name = models.CharField(max_length=100, verbose_name="文字信息")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="商品价格")
    inventory = models.IntegerField(default=100, null=False, verbose_name='库存')
    sales = models.IntegerField(default=0, null=False, verbose_name='销量')
    discount = models.CharField(max_length=100, verbose_name="折扣")

    class Meta:
        db_table = 'myshop_livetv'

    def __str__(self):
        return self.name

# 今日优惠与tv热模型基类
class PerferAndHot(models.Model):
    goodsid = models.IntegerField(default=0, null=False, verbose_name='商品id')
    img = models.CharField(max_length=255, verbose_name="图片信息")
    name = models.CharField(max_length=100, verbose_name="文字信息")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="商品价格")
    inventory = models.IntegerField(default=100, null=False, verbose_name='库存')
    sales = models.IntegerField(default=0, null=False, verbose_name='销量')
    comments = models.IntegerField(default=100, verbose_name='评论')
    introduce = models.CharField(max_length=1000, default='', verbose_name="商品介绍")
    frombrand = models.CharField(max_length=20, default='', null=True, verbose_name='所属品牌')

    class Meta:
        abstract = True


class PerferModel(PerferAndHot):
    class Meta:
        db_table = 'myshop_todayperfer'

    def __str__(self):
        return self.name


class TvHot(PerferAndHot):
    class Meta:
        db_table = 'myshop_tvhot'

    def __str__(self):
        return self.name


# 头条模型
class ShopNews(models.Model):
    type = models.CharField(null=False, max_length=255, verbose_name="新闻类型")
    title = models.CharField(null=False, max_length=100, verbose_name="文章标题")
    links = models.CharField(null=False, default='#', max_length=300, verbose_name='文章路径')

    class Meta:
        db_table = 'myshop_news'



# 商品分类模型
class FoodType(models.Model):
    typeid = models.IntegerField(verbose_name="商品分类id")
    typename = models.CharField(max_length=100, verbose_name="商品分类名称")
    childtypename = models.CharField(max_length=500, verbose_name="子分类的名称")
    childtypeid = models.IntegerField(verbose_name="子分类的id")
    brand = models.CharField(max_length=500, verbose_name="推荐品牌")
    activityid = models.IntegerField(verbose_name="热门活动id")
    titlepage = models.CharField(max_length=100, default='', verbose_name="封面图片")

    class Meta:
        db_table = 'myshop_goodstype'

    def __str__(self):
        return self.typename


# 商品模型
class Goods(models.Model):
    goodsid = models.IntegerField(verbose_name="商品id")
    img = models.CharField(max_length=100, verbose_name="商品图片")
    name = models.CharField(max_length=200, verbose_name="商品短名称")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="售价")
    comments = models.IntegerField(default=100, verbose_name='评论')
    categoryid = models.IntegerField(verbose_name="所属分类id")
    childcid = models.IntegerField(verbose_name="所属子分类id")
    childcidname = models.CharField(max_length=100, verbose_name="自分类名称")
    inventory = models.IntegerField(verbose_name="库存")
    sales = models.IntegerField(verbose_name="销量")
    introduce = models.CharField(max_length=1000, default='', verbose_name="商品介绍")
    frombrand = models.CharField(max_length=20, default='', null=True, verbose_name='所属品牌')

    class Meta:
        db_table = 'myshop_goods'

    def __str__(self):
        return self.name



# “马踏飞燕”多功能太阳镜HG186+马踏飞多功能太阳镜EG2010# 防蓝光眼镜DG501+提醒器+车载眼镜夹# 1.主品1:多功能太阳镜HG186;材质:镜片为TAC材质的偏光片、镜架为TR90塑胶钛/0.5毫米钢片;重量:约17.6g;颜色：镜片上绿下黄；灰色镜架，银灰色镜腿；尺寸：镜片宽约62mm，鼻梁宽约15mm，镜腿长约130mm；类别：遮阳镜2类 2.主品2：马踏飞燕时尚偏光镜EG2010；材质：镜片为TAC材质的偏光片 ，镜架为PC树脂；重量：约29.1g；颜色：茶色镜片，樱花色镜架；尺寸：镜片宽约50mm，鼻梁宽约23mm，镜腿长约140mm；类别：遮阳镜3类；偏光功能：有 3.赠品1:浅色太阳镜DG501;材质:镜片为树脂片、镜架为TR90塑胶钛;重量:约14.3g;颜色:黄色镜片;黑色镜架;尺寸:镜片宽约52mm,鼻梁宽约20mm,镜腿长约135mm;类别:浅色太阳镜Ⅰ类;4.赠品2:提醒器：6.8*5*2.4cm;重量18.2g;颜色：银色;5.赠品3:新型车载眼镜夹;材质:塑料;重量:约14.3g;颜色:黑色;尺寸:6.7*3.6*2.4cm;产地：浙江杭州# 1.全能太阳镜=偏光镜+遮阳镜+夜视镜 白天防太阳强光，紫外线，晚上防眩光，增强路面清晰度，确保行车安全。 2.更轻更薄，过滤眩光效果更好，榔头砸不碎，并更有韧性。 3. 多功能太阳镜镜架采用弹性不锈钢与塑胶钛结合； 套镜镜架、防蓝光眼镜均采用塑胶钛，都十分轻盈.


# 热门活动模型
class HotActivitys(models.Model):
    activityid = models.IntegerField(verbose_name="热门活动id")
    img = models.CharField(max_length=150, verbose_name="活动图片信息")
    links = models.CharField(max_length=150, verbose_name="活动路径")

    class Meta:
        db_table = 'myshop_activities'

