# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-10-03 09:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0003_auto_20191003_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255, verbose_name='新闻类型')),
                ('title', models.CharField(max_length=100, verbose_name='文章标题')),
                ('links', models.CharField(default='#', max_length=300, verbose_name='文章路径')),
            ],
            options={
                'db_table': 'myshop_news',
            },
        ),
    ]
