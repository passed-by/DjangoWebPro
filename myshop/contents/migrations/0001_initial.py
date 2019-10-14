# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-10-03 08:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LiveTV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=255, verbose_name='图片信息')),
                ('actiontime', models.CharField(max_length=100, verbose_name='直播时间')),
                ('name', models.CharField(max_length=100, verbose_name='文字信息')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='商品价格')),
                ('discount', models.CharField(max_length=100, verbose_name='折扣')),
            ],
            options={
                'db_table': 'myshop_livetv',
            },
        ),
        migrations.CreateModel(
            name='MyShopWheel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=255, verbose_name='图片信息')),
                ('name', models.CharField(max_length=100, verbose_name='文字信息')),
            ],
            options={
                'db_table': 'myshop_wheel',
            },
        ),
        migrations.CreateModel(
            name='PerferModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=255, verbose_name='图片信息')),
                ('name', models.CharField(max_length=100, verbose_name='文字信息')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='商品价格')),
                ('discount', models.CharField(default='无', max_length=100, verbose_name='折扣')),
            ],
            options={
                'db_table': 'myshop_todayperfer',
            },
        ),
        migrations.CreateModel(
            name='TvHot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=255, verbose_name='图片信息')),
                ('name', models.CharField(max_length=100, verbose_name='文字信息')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='商品价格')),
                ('discount', models.CharField(default='无', max_length=100, verbose_name='折扣')),
            ],
            options={
                'db_table': 'myshop_tvhot',
            },
        ),
    ]