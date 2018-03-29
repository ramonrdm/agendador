# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib import admin
from django.core.exceptions import ValidationError
from datetime import date

class Unidade(models.Model):
    sigla = models.CharField(max_length=20, unique=True)
    nome = models.TextField()
    unidadePai = models.ForeignKey('self', blank=True, null=True, default=1, verbose_name='Unidade pai', on_delete=models.PROTECT)
    grupos = models.ManyToManyField(Group, blank=True)
    responsavel = models.ManyToManyField(User, verbose_name='Responsáveis')
    descricao = models.TextField(verbose_name='Descrição')
    logoLink = models.URLField(blank=True, verbose_name='Link para a logo')

    def clean(self):
        errors={}
        try:
            self.check_sigla(errors)
            if self.logoLink:
                self.check_logoLink(errors)
        except:
            pass
        if bool(errors):
            raise ValidationError(errors)

    def check_logoLink(self, errors):
        image_extensions = ['jpg', 'jpeg', 'png']
        link = self.logoLink.split('.')
        extension = link[-1]
        if extension not in image_extensions:
            errors['logoLink'] = 'Insira uma imagem em uma extensão válida: %s' % ', '.join(map(str, image_extensions))


    def check_sigla(self, errors):
        if ' ' in self.sigla:
            errors['sigla'] = "Uso de espaço não permitido. Troque por ' - '."

    def __unicode__(self):
        return self.sigla
    def __str__(self):
        return self.sigla

class Atividade(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.TextField(verbose_name='Descrição')

    def __unicode__(self):
        return self.nome
    def __str__(self):
        return self.nome

class Locavel(models.Model):
    class Meta:
        abstract = True

    nome = models.TextField()
    descricao = models.TextField(verbose_name='Descrição')
    responsavel = models.ManyToManyField(User, verbose_name='Responsáveis')
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT)
    grupos = models.ManyToManyField(Group, blank=True, verbose_name='Grupos que podem reservar automaticamente')
    somenteGrupo = models.BooleanField(default=False, verbose_name='Apenas membros do grupo podem pedir reserva')
    bloqueado = models.BooleanField(default=False)
    invisivel = models.BooleanField(default=False, verbose_name='Invisível')
    permissaoNecessaria = models.BooleanField(default=False, verbose_name='Reservar somente com autorização de um responsável')
    antecedenciaMinima = models.PositiveSmallIntegerField(default=0, verbose_name='Antecedência mínima')
    antecedenciaMaxima = models.PositiveIntegerField(default=0, verbose_name='Antecedência máxima')
    localizacao = models.TextField(verbose_name='Localização')
    fotoLink = models.URLField(blank=True, verbose_name='Link para foto')
    atividadesPermitidas = models.ManyToManyField(Atividade, verbose_name='Atividades permitidas')

    def clean(self):
        errors={}
        try:
            if self.fotoLink:
                self.check_fotoLink(errors)
        except:
            pass
        if bool(errors):
            raise ValidationError(errors)

    def check_fotoLink(self, errors):
        image_extensions = ['jpg', 'jpeg', 'png']
        link = self.fotoLink.split('.')
        extension = link[-1]
        if extension not in image_extensions:
            errors['fotoLink'] = 'Insira uma imagem em uma extensão válida: %s' % ', '.join(map(str, image_extensions))

    def __unicode__(self):
        return self.nome
    def __str__(self):
        return self.nome

class EspacoFisico(Locavel):
    class Meta:
        verbose_name = 'Espaço físico'
        verbose_name_plural = 'Espaços físicos'

    capacidade = models.PositiveSmallIntegerField()

    def clean(self):
        super(EspacoFisico, self).clean()


class Equipamento(Locavel):
    patrimonio = models.PositiveIntegerField(verbose_name='Patrimônio')

    def clean(self):
        super(Equipamento, self).clean()

class Servico(Locavel):
    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    profissionais = models.ManyToManyField(User, verbose_name='Profissionais que executam o serviço', related_name='profissionais')
    def clean(self):
        super(Servico, self).clean()


class ReservaRecorrente(models.Model):
    dataInicio = models.DateField(blank=True, null=True)
    dataFim = models.DateField(blank=True, null=True)

    def update_fields(self, new_date):
        for reserve in self.get_reserves():
            if self.dataInicio > new_date:
                self.dataInicio = new_date
            elif self.dataFim < new_date:
                self.dataFim = new_date

        self.save()

    def get_reserves(self):
        query = self.reservaespacofisico_set.all()
        if not query:
            query = self.reservaequipamento_set.all()
        if not query:
            query = self.reservaservico_set.all()
        return query

    def get_days(self):
        week_days = list()
        reserves = self.get_reserves()
        for reserve in reserves:
            reserve_week_day = reserve.data.weekday()
            if reserve_week_day not in week_days:
                week_days.append(reserve_week_day)
        return week_days


class Reserva(models.Model):
    class Meta:
        abstract = True

    estados = (('A','Aprovado'),('D','Desaprovado'),('E','Esperando'), ('C', 'Cancelado'))
    estado = models.CharField(max_length=1, choices=estados, default='E')
    recorrencia = models.ForeignKey(ReservaRecorrente, blank=True, null=True, default=None, on_delete=models.PROTECT)
    data = models.DateField()
    horaInicio = models.TimeField(verbose_name='Hora início')
    horaFim = models.TimeField(verbose_name='Hora fim')
    dataReserva = models.DateTimeField(auto_now_add=True)
    atividade = models.ForeignKey(Atividade, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.PROTECT)
    ramal = models.PositiveIntegerField()
    finalidade = models.TextField()

    def clean(self):
        errors = {}
        try:
            if self.estado!='D' and self.estado!='C':
                self.verificaChoque(errors)
            self.verificaBloqueado(errors)
            self.verificaCoerencia(errors)
            if self.usuario not in self.locavel.responsavel.all():
                self.verificaAntecedencia(errors)
        except:
            pass
        if bool(errors):
            raise ValidationError(errors)

    def verificaCoerencia(self, errors):
        if date.today() > self.data:
            errors['data'] = 'Não é possível reservar em datas passadas.'
        if self.horaInicio > self.horaFim:
            errors['horaInicio'] = 'Horário incoerente.'
            errors['horaFim'] = 'Horário incoerente.'

    def verificaAntecedencia(self, errors):
        if self.locavel.antecedenciaMinima != 0:
            antecedencia = (self.data - date.today()).days
            if antecedencia < self.locavel.antecedenciaMinima:
                errors['data'] = 'Este locável tem antecedência mínima de %d dias.' % (self.locavel.antecedenciaMinima, )
        if self.locavel.antecedenciaMaxima != 0:
            antecedencia = (self.data - date.today()).days
            if antecedencia > self.locavel.antecedenciaMaxima:
                errors['data'] = 'Este locável tem antecedência máxima de %d dias.' % (self.locavel.antecedenciaMaxima, )

    def verificaBloqueado(self, errors):
        # Check if superuser
        responsable = self.usuario.is_superuser
        # Check if responsable for locable
        locable_responsables = self.locavel.responsavel.all()
        for locable_responsable in locable_responsables:
            if locable_responsable.id == self.usuario.id:
                responsable = True
        # Check if unit responsable
        if self.usuario in self.locavel.unidade.responsavel.all():
            responsable = True

        if self.locavel.bloqueado and not responsable:
            error = " Locavel " + self.locavel.nome + ' bloqueado.'
            errors['locavel'] = error

    # Ignore variables is for recurrent test, there's no need to check self conflict
    def verificaChoque(self, errors, ignore=[]):
        reservas = type(self).objects.filter(locavel=self.locavel, data=self.data, estado="A").exclude(id=self.id)
        for reserve in ignore:
            try:
                reservas = reservas.exclude(id=reserve.id)
            except:
                pass  # if we can't exclude from the query it means it's already not there

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
    class Meta:
        verbose_name = 'Reserva espaço físico'
        verbose_name_plural = 'Reservas espaços físicos'

    locavel = models.ForeignKey(EspacoFisico, verbose_name='Locável', on_delete=models.PROTECT)

    def clean(self):
        super(ReservaEspacoFisico, self).clean()

    def __unicode__(self):
        return self.usuario.username+"/"+self.atividade.nome


class ReservaEquipamento(Reserva):
    locavel = models.ForeignKey(Equipamento, verbose_name='Locável', on_delete=models.PROTECT)

    def clean(self):
        super(ReservaEquipamento, self).clean()

    def __unicode__(self):
        return self.usuario.username+"/"+self.atividade.nome

class ReservaServico(Reserva):
    class Meta:
        verbose_name = 'Reserva serviço'
        verbose_name_plural = 'Reserva serviços'

    locavel = models.ForeignKey(Servico, verbose_name='Locável', on_delete=models.PROTECT)

    def clean(self):
        super(ReservaServico, self).clean()

    def __unicode__(self):
        return self.usuario.username+"/"+self.atividade.nome