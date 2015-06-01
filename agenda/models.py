from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Equipamento(models.Model):
	nome = models.TextField()
	patrimonio = models.PositiveIntegerField()
	responsavel = models.ForeignKey(User)
	#bloqueado?
	#visivel?
	def __unicode__(self):
		return self.nome

class Centro(models.Model):
	nome = models.TextField()
	sigla = models.CharField(max_length=10)


class Departamento(models.Model):
	sigla = models.CharField(max_length=5)
	descricao = models.TextField()
	Centro = models.ForeignKey(Centro)

	def __unicode__(self):
		return self.sigla

class TipoEvento(models.Model):
	nome = models.CharField(max_length=30)
	descricao = models.TextField()

	def __unicode__(self):
		return self.nome

class EspacoFisico(models.Model):
	nome = models.TextField()
	centro = models.ForeignKey(Centro)
	departamento = models.ForeignKey(Departamento)
	descricao = models.TextField()
	capacidade = models.PositiveSmallIntegerField()
	eventosPermitidos = models.ManyToManyField(TipoEvento)
	responsavel = models.ForeignKey(User)
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
	departamento = models.ForeignKey(Departamento)
	finalidade = models.TextField()
	#bloqueado?
	#visivel?
	
	def __unicode__(self):
		return self.usuario.username+"/"+self.departamento.sigla+" - "+self.evento.nome

