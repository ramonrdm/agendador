# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Grupo(models.Model):
	sigla = models.CharField(max_length=10)
	nome = models.TextField()
	grupoPai = models.ForeignKey('self', blank=True, null=True, default=1)
	responsavel = models.ForeignKey(User)
	descricao = models.TextField()
	logo = models.FileField(blank=True)

	def __unicode__(self):
		return self.sigla

class Evento(models.Model):
	nome = models.CharField(max_length=30)
	descricao = models.TextField()

	def __unicode__(self):
		return self.nome

class Locavel(models.Model):
	class Meta:
		abstract = True

	nome = models.TextField()
	descricao = models.TextField()
	responsavel = models.ForeignKey(User)
	grupo = models.ForeignKey(Grupo)
	bloqueado = models.BooleanField(default=False)
	visivel = models.BooleanField(default=False)
	localizacao = models.TextField()
	def __unicode__(self):
		return self.nome

class EspacoFisico(Locavel):
	capacidade = models.PositiveSmallIntegerField()
	eventosPermitidos = models.ManyToManyField(Evento)

class Equipamento(Locavel):
	patrimonio = models.PositiveIntegerField()

class Reserva(models.Model):
	class Meta:
		abstract = True
	
	estado = models.CharField(max_length=1)
	data = models.DateField()
	horaInicio = models.TimeField()
	horaFim = models.TimeField()
	dataReserva  = models.DateTimeField(auto_now_add=True)
	evento = models.ForeignKey(Evento)
	usuario = models.ForeignKey(User)
	ramal = models.PositiveIntegerField()
	grupo = models.ForeignKey(Grupo)
	finalidade = models.TextField()
	
	def __unicode__(self):
		return self.usuario.username+"/"+self.Grupo.sigla+" - "+self.evento.nome

class ReservaEspacoFisico(Reserva):
	espacoFisico = models.ForeignKey(EspacoFisico)


class ReservaEquipamento(Reserva):
	espacoFisico = models.ForeignKey(Equipamento)

