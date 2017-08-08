# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0005_auto_20170624_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservaequipamento',
            name='estado',
            field=models.CharField(default=b'E', max_length=1, choices=[(b'A', b'Aprovado'), (b'D', b'Desaprovado'), (b'E', b'Esperando')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reservaespacofisico',
            name='estado',
            field=models.CharField(default=b'E', max_length=1, choices=[(b'A', b'Aprovado'), (b'D', b'Desaprovado'), (b'E', b'Esperando')]),
            preserve_default=True,
        ),
    ]
