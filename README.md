# DjangoWebPro
基于Django框架的电商项目

#### 使用工具
- MySQL5.7
- Pycharm profession 2019.1.3
- Redis

#### 使用Django版本
> django == 1.11.11

#### 实现功能
- 登录,注册
  - 发送手机短信 登录/注册 (使用云之讯);
  
- 商城首页面
  - 实现轮播图,数据库所有商品渲染到主页面;
  - 可点击查看商品详情;
  - 首页实现 注销 功能,注销当前登录用户;
  
- 商品详情页面
  - 根据指定商品显示商品详细信息;
  
- 购物车页面
  - 购物车页面实现从Redis获取购物车数据;
  - 页面可以增加/减少商品数量,取消商品选择状态,清空购物车;
  - 点击页面下单功能生成订单并跳转;
  
- 总订单详情页面
  - 展示所有已支付/未支付订单列表;
  - 点击订单编号可以查看订单详情;
  - 点击"支付订单"可跳转支付宝支付页面,使用支付宝沙箱账号进行支付,并在支付成功后跳转回调函数执行自定义路由;
  
- 子订单详情页面
  - 展示总订单下详细购买商品内容;
  
#### 数据库分支
**myshop**
  - myshop_goods(商品库)
  - myshop_activities(一级分类活动)
  - myshop_goodstype(商品分类库)
  - myshop_livetv(在线直播库)
  - myshop_news(新闻库)
  - myshop_order_detail(子订单库)
  - myshop_orders(总订单库)
  - myshop_todayperfer(今日推荐)
  - myshop_tvhot(tv热播)
  - myshop_users(电商用户类)
  - myshop_wheel(轮播图类)
