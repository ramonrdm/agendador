# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sigla', models.CharField(max_length=10)),
                ('nome', models.TextField()),
                ('descricao', models.TextField()),
                ('responsavel', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('setorPai', models.ForeignKey(to='agenda.Setor')),
                ('setoresFilhos', models.ManyToManyField(related_name='setoresFilhos_rel_+', to='agenda.Setor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='espacofisico',
            name='centro',
        ),
        migrations.DeleteModel(
            name='Centro',
        ),
        migrations.RemoveField(
            model_name='espacofisico',
            name='departamento',
        ),
        migrations.RemoveField(
            model_name='reserva',
            name='departamento',
        ),
        migrations.DeleteModel(
            name='Departamento',
        ),
        migrations.AddField(
            model_name='equipamento',
            name='setor',
            field=models.ForeignKey(default=1, to='agenda.Setor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='espacofisico',
            name='setor',
            field=models.ForeignKey(default=1, to='agenda.Setor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reserva',
            name='setor',
            field=models.ForeignKey(default=1, to='agenda.Setor'),
            preserve_default=False,
        ),
    ]
