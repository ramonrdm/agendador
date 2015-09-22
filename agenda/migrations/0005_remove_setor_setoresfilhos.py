# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0004_setor_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='setor',
            name='setoresFilhos',
        ),
    ]
