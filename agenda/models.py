# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib import admin
from django.core.exceptions import ValidationError

class Unidade(models.Model):
    sigla = models.CharField(max_length=10, unique=True)
    nome = models.TextField()
    unidadePai = models.ForeignKey('self', blank=True, null=True, default=1)
    grupo = models.ForeignKey(Group, blank=True, null=True)
    responsavel = models.ManyToManyField(User)
    descricao = models.TextField()
    logo = models.FileField(blank=True)

    def __unicode__(self):
        return self.sigla
    def __str__(self):
        return self.sigla

class Atividade(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.TextField()

    def __unicode__(self):
        return self.nome
    def __str__(self):
        return self.nome

class Locavel(models.Model):
    class Meta:
        abstract = True

    nome = models.TextField()
    descricao = models.TextField()
    responsavel = models.ManyToManyField(User)
    unidade = models.ForeignKey(Unidade)
    grupo = models.ForeignKey(Group, blank=True, null=True)
    bloqueado = models.BooleanField(default=False)
    visivel = models.BooleanField(default=True)
    localizacao = models.TextField()
    foto = models.FileField(blank=True)
    def __unicode__(self):
        return self.nome
    def __str__(self):
        return self.nome

class EspacoFisico(Locavel):
    capacidade = models.PositiveSmallIntegerField()
    atividadesPermitidas = models.ManyToManyField(Atividade)

class Equipamento(Locavel):
    patrimonio = models.PositiveIntegerField()

class Reserva(models.Model):
    class Meta:
        abstract = True
    
    estados = (('A','Aprovado'),('D','Desaprovado'),('E','Esperando'))
    estado = models.CharField(max_length=1, choices=estados, default='E')
    data = models.DateField()
    horaInicio = models.TimeField()
    horaFim = models.TimeField()
    dataReserva = models.DateTimeField(auto_now_add=True)
    atividade = models.ForeignKey(Atividade)
    usuario = models.ForeignKey(User)
    ramal = models.PositiveIntegerField()
    finalidade = models.TextField()
    
    def __unicode__(self):
        return self.usuario.username+"/"+self.atividade.nome

class ReservaEspacoFisico(Reserva):
    espacoFisico = models.ForeignKey(EspacoFisico)

    def __unicode__(self):
        return self.usuario.username+"/"+self.atividade.nome


class ReservaEquipamento(Reserva):
    equipamento = models.ForeignKey(Equipamento)

    def clean(self):
        super(type(self), self).clean()
        reservas = type(self).objects.filter(equipamento=self.equipamento, data=self.data)
        for r in reservas:
            print self.horaInicio
            if  (
                (self.horaFim  > r.horaInicio and self.horaFim < r.horaFim) or 
                (self.horaInicio > r.horaInicio and self.horaInicio < r.horaFim ) or 
                (self.horaInicio == r.horaInicio and self.horaFim == r.horaFim) or
                (r.horaInicio > self.horaInicio and r.horaInicio < self.horaFim) or
                (self.horaInicio < r.horaFim < self.horaFim)
                ):
                raise ValidationError({'data': 'choque!'})
            elif self.equipamento.bloqueado:
                raise ValidationError({'equipamento': 'Equipamento bloqueado'})

    def __unicode__(self):
        return self.usuario.username+"/"+self.atividade.nome

