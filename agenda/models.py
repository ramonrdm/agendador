from django.db import models

# Create your models here.
class Departamento(models.Model):
	id = models.AutoField(primary_key=True)
	sigla = models.CharField(max_length=5)
	descricao = models.TextField()

	def __unicode__(self):
		return self.sigla

class EspacoFisico(models.Model):
	id = models.AutoField(primary_key=True)
	nome = models.TextField()
	descricao = models.TextField()

	def __unicode__(self):
		return self.nome


class TipoEvento(models.Model):
	id  = models.AutoField(primary_key=True)
	nome = models.TextField()
	descricao = models.TextField()

	def __unicode__(self):
		return self.nome

class Usuario(models.Model):
	id = models.AutoField(primary_key=True)
	nome_completo = models.TextField()
	email = models.CharField(max_length=50)
	vinculo = models.PositiveSmallIntegerField()

class Reserva(models.Model):
	id = models.AutoField(primary_key=True)
	dataUsoInicio = models.DateTimeField()
	dataUsoFim = models.DateTimeField()
	dataReserva  = models.DateTimeField()
	espacoFisico = models.ForeignKey(EspacoFisico)
	tipoEvento = models.ForeignKey(TipoEvento)
	usuario = models.ForeignKey(Usuario)
	ramal = models.PositiveSmallIntegerField()
	departamento = models.ForeignKey(Departamento)
	finalidade = models.TextField()

