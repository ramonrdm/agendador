# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-20 17:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('agenda', '0003_auto_20171218_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipamento',
            name='grupo',
        ),
        migrations.RemoveField(
            model_name='espacofisico',
            name='grupo',
        ),
        migrations.RemoveField(
            model_name='unidade',
            name='grupo',
        ),
        migrations.AddField(
            model_name='equipamento',
            name='grupos',
            field=models.ManyToManyField(blank=True, null=True, to='auth.Group'),
        ),
        migrations.AddField(
            model_name='espacofisico',
            name='grupos',
            field=models.ManyToManyField(blank=True, null=True, to='auth.Group'),
        ),
        migrations.AddField(
            model_name='unidade',
            name='grupos',
            field=models.ManyToManyField(blank=True, null=True, to='auth.Group'),
        ),
    ]
