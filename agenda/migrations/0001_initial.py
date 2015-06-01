# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Centro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.TextField()),
                ('sigla', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sigla', models.CharField(max_length=5)),
                ('descricao', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Equipamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.TextField()),
                ('patrimonio', models.PositiveIntegerField()),
                ('responsavel', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EspacoFisico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.TextField()),
                ('descricao', models.TextField()),
                ('capacidade', models.PositiveSmallIntegerField()),
                ('localizacao', models.TextField()),
                ('centro', models.ForeignKey(to='agenda.Centro')),
                ('departamento', models.ForeignKey(to='agenda.Departamento')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('estado', models.CharField(max_length=1)),
                ('data', models.DateField()),
                ('horaInicio', models.TimeField()),
                ('horaFim', models.TimeField()),
                ('dataReserva', models.DateTimeField(auto_now_add=True)),
                ('ramal', models.PositiveIntegerField()),
                ('finalidade', models.TextField()),
                ('departamento', models.ForeignKey(to='agenda.Departamento')),
                ('espacoFisico', models.ForeignKey(to='agenda.EspacoFisico')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoEvento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=30)),
                ('descricao', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='reserva',
            name='evento',
            field=models.ForeignKey(to='agenda.TipoEvento'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reserva',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='espacofisico',
            name='eventosPermitidos',
            field=models.ManyToManyField(to='agenda.TipoEvento'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='espacofisico',
            name='responsavel',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
