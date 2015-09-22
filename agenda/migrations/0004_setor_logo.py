# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0003_auto_20150922_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='setor',
            name='logo',
            field=models.FileField(default=0, upload_to=b''),
            preserve_default=False,
        ),
    ]
