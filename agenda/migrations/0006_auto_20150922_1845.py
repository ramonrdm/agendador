# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agenda', '0005_remove_setor_setoresfilhos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sigla', models.CharField(max_length=10)),
                ('nome', models.TextField()),
                ('descricao', models.TextField()),
                ('logo', models.FileField(upload_to=b'')),
                ('grupoPai', models.ForeignKey(default=1, blank=True, to='agenda.Grupo', null=True)),
                ('responsavel', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='setor',
            name='responsavel',
        ),
        migrations.RemoveField(
            model_name='setor',
            name='setorPai',
        ),
        migrations.RemoveField(
            model_name='equipamento',
            name='setor',
        ),
        migrations.RemoveField(
            model_name='espacofisico',
            name='setor',
        ),
        migrations.RemoveField(
            model_name='reserva',
            name='setor',
        ),
        migrations.DeleteModel(
            name='Setor',
        ),
        migrations.AddField(
            model_name='equipamento',
            name='grupo',
            field=models.ForeignKey(default=0, to='agenda.Grupo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='espacofisico',
            name='grupo',
            field=models.ForeignKey(default=1, to='agenda.Grupo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reserva',
            name='grupo',
            field=models.ForeignKey(default=1, to='agenda.Grupo'),
            preserve_default=False,
        ),
    ]
