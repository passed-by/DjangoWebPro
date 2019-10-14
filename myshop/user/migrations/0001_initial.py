# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-10-05 02:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField(verbose_name='用户编号')),
                ('password', models.CharField(default='123456', max_length=50, verbose_name='用户密码')),
                ('phone', models.CharField(max_length=11, verbose_name='手机号')),
                ('email', models.CharField(max_length=50, null=True, verbose_name='邮箱')),
            ],
            options={
                'db_table': 'myshop_users',
            },
        ),
    ]
