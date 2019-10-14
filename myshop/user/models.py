from django.db import models

# Create your models here.
# 用户模型
class Users(models.Model):
    username = models.CharField(max_length=11,default='', null=False, verbose_name="用户名")
    userid = models.IntegerField(null=False, unique=True, verbose_name="用户编号")
    password = models.CharField(max_length=50, default='123456', null=False, verbose_name="用户密码")
    phone = models.CharField(max_length=11, null=False, verbose_name="手机号")
    email = models.CharField(max_length=50, verbose_name="邮箱", null=True)

    class Meta:
        db_table = 'myshop_users'