# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0002_auto_20150922_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setor',
            name='setorPai',
            field=models.ForeignKey(default=1, blank=True, to='agenda.Setor', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='setor',
            name='setoresFilhos',
            field=models.ManyToManyField(related_name='setoresFilhos_rel_+', null=True, to='agenda.Setor', blank=True),
            preserve_default=True,
        ),
    ]
