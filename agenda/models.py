from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Departamento(models.Model):
	id = models.AutoField(primary_key=True)
	sigla = models.CharField(max_length=5)
	descricao = models.TextField()

	def __unicode__(self):
		return self.sigla

class TipoEvento(models.Model):
	id  = models.AutoField(primary_key=True)
	nome = models.CharField(max_length=30)
	descricao = models.TextField()

	def __unicode__(self):
		return self.nome

class EspacoFisico(models.Model):
	id = models.AutoField(primary_key=True)
	nome = models.TextField()
	descricao = models.TextField()
	capacidade = models.PositiveSmallIntegerField()
	eventosPermitidos = models.ManyToManyField(TipoEvento)

	def __unicode__(self):
		return self.nome
		
class Reserva(models.Model):
	id = models.AutoField(primary_key=True)
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
	
	def __unicode__(self):
		return self.finalidade

