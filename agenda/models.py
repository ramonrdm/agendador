# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Setor(models.Model):
	sigla = models.CharField(max_length=10)
	nome = models.TextField()
	setorPai = models.ForeignKey('self', blank=True, null=True, default=1)
	responsavel = models.ForeignKey(User)
	descricao = models.TextField()
	logo = models.FileField()

	def __unicode__(self):
		return self.sigla

class Equipamento(models.Model):
	nome = models.TextField()
	patrimonio = models.PositiveIntegerField()
	responsavel = models.ForeignKey(User)
	setor = models.ForeignKey(Setor)
	#bloqueado?
	#visivel?
	def __unicode__(self):
		return self.nome

class TipoEvento(models.Model):
	nome = models.CharField(max_length=30)
	descricao = models.TextField()

	def __unicode__(self):
		return self.nome

class EspacoFisico(models.Model):
	nome = models.TextField()
	descricao = models.TextField()
	capacidade = models.PositiveSmallIntegerField()
	eventosPermitidos = models.ManyToManyField(TipoEvento)
	responsavel = models.ForeignKey(User)
	setor = models.ForeignKey(Setor)
	localizacao = models.TextField()

	def __unicode__(self):
		return self.nome
		
class Reserva(models.Model):
	estado = models.CharField(max_length=1)
	data = models.DateField()
	horaInicio = models.TimeField()
	horaFim = models.TimeField()
	dataReserva  = models.DateTimeField(auto_now_add=True)
	espacoFisico = models.ForeignKey(EspacoFisico)
	evento = models.ForeignKey(TipoEvento)
	usuario = models.ForeignKey(User)
	ramal = models.PositiveIntegerField()
	setor = models.ForeignKey(Setor)
	finalidade = models.TextField()
	#bloqueado?
	#visivel?
	
	def __unicode__(self):
		return self.usuario.username+"/"+self.setor.sigla+" - "+self.evento.nome

