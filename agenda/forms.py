# -*- coding: utf-8 -*-

from agenda.models import Reserva, EspacoFisico, ReservaEspacoFisico, ReservaEquipamento, Equipamento, Atividade
from django import forms
from django.contrib.admin import widgets
import datetime
from django.core.mail import send_mail
from django.forms import ModelForm, Form, HiddenInput, models, fields
from django.contrib.admin.sites import AdminSite
from django.core.exceptions import ValidationError
from django.contrib.admin import widgets
from django.forms.widgets import Select
from widgets import *
from django.contrib.auth.models import User
from django.db.models.fields.related import ManyToOneRel
import admin

class ReservaAdminForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(ReservaAdminForm, self).__init__(*args, **kwargs)

        # Check if there's been errors in custom widget, since we're using an automated template for form's HTML that doesn't display them 
        # errors must be displayed through the custom Widget in order to appear
        attrs = {}
        if 'horaInicio' in self.errors:
            attrs['error'] = self.errors['horaInicio']
        self.fields['horaInicio'] = forms.TimeField(input_formats=['%H:%M'], widget=SelectTimeWidget(attrs=attrs))

        attrs = {}
        if 'horaFim' in self.errors:
            attrs['error'] = self.errors['horaFim']
        self.fields['horaFim'] = forms.TimeField(input_formats=['%H:%M'], widget=SelectTimeWidget(attrs=attrs))
        try:
            self.fields['data'].initial = self.request.session['data']
        except:
            pass
        self.request.session['data'] = ''
        try:
            self.fields['horaInicio'].initial = self.request.session['horaInicio']
            self.fields['horaFim'].initial = self.request.session['horaFim']
        except:
            pass
        self.request.session['horaInicio'] = ''
        self.request.session['horaFim'] = ''
        if not self.request.user.is_superuser:
            self.fields['usuario'].initial = self.request.user
            self.fields['usuario'].widget = forms.HiddenInput()
            self.fields['usuario'].label = ''
        else:
            attrs = {}
            if 'usuario' in self.errors:
                attrs['error'] = self.errors['usuario']
            self.fields['usuario'].widget = AutocompleteWidget(attrs=attrs, query=User.objects.all(), model=User)

        # If we're creating a new form it's okay to hide the status. If we're additing an existing one, it mus show status if user is reponsable
        hide = False
        if 'instance' in kwargs:
            if kwargs['instance']:
                reservable = kwargs['instance'].locavel
                # Check what's the model and reservables the user own
                if isinstance(reservable, EspacoFisico):
                    reservable_set = self.request.user.espacofisico_set.all()
                elif isinstance(reservable, Equipamento):
                    reservable_set = self.request.user.equipamento_set.all()
                if reservable not in reservable_set:
                    hide = True
        else:
            hide = True
        if hide and not self.request.user.is_superuser:
            self.fields['estado'].initial = 'E'
            self.fields['estado'].widget = forms.HiddenInput()
            self.fields['estado'].label = ''

    def sendMail(self, status, instance):
        user = instance.usuario
        status = instance.estado
        reservable = instance.locavel
        date = instance.data
        start = instance.horaInicio
        end = instance.horaFim
        responsables = reservable.responsavel.all()
        # First we send an email to the user who asked for the reserve
        if status == 'A':
            email_title = 'Reserva de %s confirmada.' % reservable
            email_text = '''
                Olá, %s,
                Sua reserva de %r dia %s, das %s às %s, foi confirmada.

                -------
                E-mail automático, por favor não responda.
            ''' % (user, reservable.nome, date.strftime('%d/%m/%Y'), start.strftime('%H:%M'), end.strftime('%H:%M'))
        elif status == 'E':
            email_title = 'Reserva de %s aguardando aprovação.' % reservable
            email_text = '''
                Olá, %s,
                Sua reserva de %r dia %s, das %s às %s, está aguardando aprovação. Você receberá uma notificação quando o estado da sua reserva for atualizado.

                -------
                E-mail automático, por favor não responda.
            ''' % (user, reservable, date.strftime('%d/%m/%Y'), start.strftime('%H:%M'), end.strftime('%H:%M'))
        elif status == 'D':
            email_title = 'Reserva de %s negada.' % reservable
            email_text = '''
                Olá, %s,
                Sua reserva de %r dia %s, das %s às %s, foi negada.

                -------
                E-mail automático, por favor não responda.
            ''' % (user, reservable, date.strftime('%d/%m/%Y'), start.strftime('%H:%M'), end.strftime('%H:%M'))
        # send_mail(email_title, email_text, 'noreply@reservasufsc.com', [user.email])

        # If the user doesn't have permission we need to send a e-mail to the reservable responsable
        if status == 'E':
            # Need to check reservable instance to genereate the link 
            if isinstance(reservable, EspacoFisico):
                reserve_type = 'reservaespacofisico'
            elif isinstance(reservable, Equipamento):
                reserve_type = 'reservaequipamento'

            for responsable in responsables:
                email_title = 'Pedido de reserva de %s' % reservable
                email_text = '''
                    Olá, %s,
                    %s fez um pedido de reserva em %r, dia %s, das %s às %s. Use o link abaixo para analisar o pedido.
                    http://reservas.cce.ufsc.br/admin/agenda/%s/%d/change/

                    -------
                    E-mail automático, por favor não responda.
                ''' % (responsable, user, reservable, date.strftime('%d/%m/%Y'), start.strftime('%H:%M'), end.strftime('%H:%M'), reserve_type, instanceid)
                #send_mail(email_title, email_text, 'noreply@reservasufsc.com', [responsable.email])

    def save(self, *args, **kwargs):
        user_query = kwargs.pop('query', None)
        reservable = self.cleaned_data['locavel']
        instance = super(ReservaAdminForm, self).save(commit=False)

        # Check if the user has permission in this reservable
        # If it is, the reserve is automatically accepted
        if reservable in user_query:
            status = 'A'
        instance.estado = status
        instance.save()
        self.sendMail(status, instance)
        return instance

class ReservaEquipamentoAdminForm(ReservaAdminForm):
    class Meta:
        model = ReservaEquipamento
        fields = ('estado', 'data', 'horaInicio', 'horaFim', 'locavel', 'atividade', 'usuario', 'ramal', 'finalidade')
    def __init__(self, *args, **kwargs):
        super(ReservaEquipamentoAdminForm, self).__init__(*args, **kwargs)
        # In case there's an error the old pre-selected reservable must be recovered
        if self.errors:
            try:
                self.request.session['id_equip'] = self.request.session['id_equip_backup']
            except:
                pass

        try:
            self.id_equip = self.request.session['id_equip']
        except:
            self.id_equip = None
        ma = admin.EquipamentoAdmin(Equipamento, AdminSite())
        queryset = ma.get_queryset(self.request)
        if self.id_equip:
            self.fields['locavel'].initial = self.id_equip
            self.fields['locavel'].queryset = Equipamento.objects.filter(id=self.id_equip)
            self.fields['atividade'].queryset = Equipamento.objects.get(id=self.id_equip).atividadesPermitidas
        else:
            self.fields['locavel'].queryset = queryset
        rel = Reserva._meta.get_field('atividade').rel
        self.fields['atividade'].widget = DynamicAtividadeWidget(Select(choices=models.ModelChoiceIterator(self.fields['atividade'])), rel, admin.admin.site, can_change_related=True)
        
        # id_equip is saved so it can be recovered in case of errors
        self.request.session['id_equip_backup'] = self.id_equip
        self.request.session['id_equip'] = None

    def save(self, *args, **kwargs):
        temp_request = self.request
        temp_request.user = self.cleaned_data['usuario']
        ma = admin.EspacoFisicoAdmin(Equipamento, AdminSite())
        user_query = ma.get_queryset(temp_request)
        kwargs['query'] = user_query
        return super(ReservaEquipamentoAdminForm, self).save(*args, **kwargs)


class ReservaEspacoFisicoAdminForm(ReservaAdminForm):
    class Meta:
        model = ReservaEspacoFisico
        fields = ('estado', 'data', 'horaInicio', 'horaFim', 'locavel', 'atividade', 'usuario', 'ramal', 'finalidade')
    def __init__(self, *args, **kwargs):
        super(ReservaEspacoFisicoAdminForm, self).__init__(*args, **kwargs)
        # In case there's an error the old pre-selected reservable must be recovered
        if self.errors:
            try:
                self.request.session['id_equip'] = self.request.session['id_equip_backup']
            except:
                pass

        try:
            self.id_equip = self.request.session['id_equip']
        except:
            self.id_equip = None
        ma = admin.EspacoFisicoAdmin(EspacoFisico, AdminSite())
        queryset = ma.get_queryset(self.request)
        if self.id_equip:
            self.fields['locavel'].initial = self.id_equip
            self.fields['locavel'].queryset = EspacoFisico.objects.filter(id=self.id_equip)
            self.fields['atividade'].queryset = EspacoFisico.objects.get(id=self.id_equip).atividadesPermitidas
        else:
            self.fields['locavel'].queryset = queryset
        rel = Reserva._meta.get_field('atividade').rel
        self.fields['atividade'].widget = DynamicAtividadeWidget(Select(choices=models.ModelChoiceIterator(self.fields['atividade'])), rel, admin.admin.site, can_change_related=True)

        # id_equip is saved so it can be recovered in case of errors
        self.request.session['id_equip_backup'] = self.id_equip
        self.request.session['id_equip'] = None

    def save(self, *args, **kwargs):
        temp_request = self.request
        temp_request.user = self.cleaned_data['usuario']
        ma = admin.EspacoFisicoAdmin(EspacoFisico, AdminSite())
        user_query = ma.get_queryset(self.request)
        kwargs['query'] = user_query
        return super(ReservaEspacoFisicoAdminForm, self).save(*args, **kwargs) 

class SearchFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        try:
            self.tipo_init = kwargs.pop('tipo')
            super(SearchFilterForm,self).__init__(*args,**kwargs)
            self.fields['tipo'].initial = self.tipo_init
        except:
            super(SearchFilterForm,self).__init__(*args,**kwargs)

    data = forms.DateField(input_formats=['%d/%m/%Y'], widget=SelectDateWidget())
    data.label = ''
    horaInicio = forms.TimeField(input_formats=['%H:%M'], widget=SelectTimeWidget())
    horaInicio.label = ''
    horaFim = forms.TimeField(input_formats=['%H:%M'], widget=SelectTimeWidget())
    horaFim.label = ''
    tipo = forms.CharField(widget = forms.HiddenInput())

    def clean(self):
        cleaned_data = super(SearchFilterForm, self).clean()
