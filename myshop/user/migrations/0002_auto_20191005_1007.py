# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-10-05 02:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='userid',
            field=models.IntegerField(unique=True, verbose_name='用户编号'),
        ),
    ]
