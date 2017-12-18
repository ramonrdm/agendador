# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib import admin
from django.core.exceptions import ValidationError
from datetime import date

class Unidade(models.Model):
    sigla = models.CharField(max_length=20, unique=True)
    nome = models.TextField()
    unidadePai = models.ForeignKey('self', blank=True, null=True, default=1)
    grupo = models.ForeignKey(Group, blank=True, null=True)
    responsavel = models.ManyToManyField(User)
    descricao = models.TextField()
    logoLink = models.URLField(blank=True)

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
    invisivel = models.BooleanField(default=False)
    localizacao = models.TextField()
    fotoLink = models.URLField(blank=True)
    atividadesPermitidas = models.ManyToManyField(Atividade)
    def __unicode__(self):
        return self.nome
    def __str__(self):
        return self.nome

class EspacoFisico(Locavel):
    capacidade = models.PositiveSmallIntegerField()
    

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

    def clean(self):
        errors = {}
        try:
            self.verificaChoque(errors)
            self.verificaBloqueado(errors)
            self.verificaCoerencia(errors)
        except:
            pass
        if bool(errors):
            print errors
            raise ValidationError(errors)

    def verificaCoerencia(self, errors):
        print date.today()
        if self.horaInicio > self.horaFim or date.today() > self.data:
            errors['data'] = 'Data e/ou hora incoerente'

    def verificaBloqueado(self, errors):
        class MockRequest:
            pass
        request = MockRequest()
        request.user = self.usuario
        # Check if superuser
        responsable = self.usuario.is_superuser
        # Check if responsable for locable
        locable_responsables = self.locavel.responsavel.all()
        for locable_responsable in locable_responsables:
            if locable_responsable.id == self.usuario.id:
                responsable = True
        # Check if unit responsable
        unit_responsables = self.locavel.unidade.responsavel.all()
        ma = adm.UnidadeAdmin(Unidade, admin.sites.AdminSite())
        queryset = ma.get_queryset(request)
        if self.locavel.unidade in queryset:
            responsable = True

        if self.locavel.bloqueado and not responsable:
            error = " Locavel " + self.locavel.nome + ' bloqueado.'
            errors['locavel'] = error

    def verificaChoque(self, errors):
        reservas = type(self).objects.filter(locavel=self.locavel, data=self.data).exclude(id=self.id)
        for r in reservas:
            if  (
                (self.horaFim  > r.horaInicio and self.horaFim < r.horaFim) or 
                (self.horaInicio > r.horaInicio and self.horaInicio < r.horaFim ) or 
                (self.horaInicio == r.horaInicio and self.horaFim == r.horaFim) or
                (r.horaInicio > self.horaInicio and r.horaInicio < self.horaFim) or
                (self.horaInicio < r.horaFim < self.horaFim)
                ):
                errors['data'] = 'Já existem reservas para esse dia e hora'
    
    def __unicode__(self):
        return self.usuario.username+"/"+self.atividade.nome

class ReservaEspacoFisico(Reserva):
    locavel = models.ForeignKey(EspacoFisico)
    
    def clean(self):
        super(ReservaEspacoFisico, self).clean()

    def __unicode__(self):
        return self.usuario.username+"/"+self.atividade.nome


class ReservaEquipamento(Reserva):
    locavel = models.ForeignKey(Equipamento)

    def clean(self):
        super(ReservaEquipamento, self).clean()

    def __unicode__(self):
        return self.usuario.username+"/"+self.atividade.nome

import admin as adm