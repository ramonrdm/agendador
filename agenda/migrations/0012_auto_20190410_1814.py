# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-10 18:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0011_auto_20190404_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipamento',
            name='limite_horas',
            field=models.TimeField(default=datetime.time(0, 0), verbose_name=b'Limite de Horas por Usu\xc3\xa1rio'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='periodo_limite',
            field=models.IntegerField(default=0),
        ),
    ]
