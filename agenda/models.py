from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

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
	capacidade = models.PositiveSmallIntegerField()

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
	def __unicode__(self):
		return self.nome_completo

class Reserva(models.Model):
	id = models.AutoField(primary_key=True)
	estado = models.CharField(max_length=1)
	#idufsc = models.CharField(max_length=100)
	dataUsoInicio = models.DateTimeField()
	dataUsoFim = models.DateTimeField()
	dataReserva  = models.DateTimeField()
	espacoFisico = models.ForeignKey(EspacoFisico)
	tipoEvento = models.ForeignKey(TipoEvento)
	usuario = models.ForeignKey(Usuario)
	ramal = models.PositiveSmallIntegerField()
	departamento = models.ForeignKey(Departamento)
	finalidade = models.TextField()
	
	def __unicode__(self):
		return self.finalidade



class Entry(models.Model):
    title = models.CharField(max_length=40)
    snippet = models.CharField(max_length=150, blank=True)
    body = models.TextField(max_length=10000, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField(blank=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    remind = models.BooleanField(default=False)

    def __unicode__(self):
        if self.title:
            return unicode(self.creator) + u" - " + self.title
        else:
            return unicode(self.creator) + u" - " + self.snippet[:40]

    def short(self):
        if self.snippet:
            return u"<i>%s</i> - %s" % (self.title, self.snippet)
        else:
            return self.title
    short.allow_tags = True

    class Meta:
        verbose_name_plural = "entries"


### Admin

class EntryAdmin(admin.ModelAdmin):
    list_display = ["creator", "date", "title", "snippet"]
    search_fields = ["title", "snippet"]
    list_filter = ["creator"]