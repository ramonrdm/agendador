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
        self.admin_type = kwargs.pop('admin_type', None)
        self.reservable_type = kwargs.pop('reservable_type', None)
        super(ReservaAdminForm, self).__init__(*args, **kwargs)

        # If the user is trying to edit a reserve for a reservable not being responsable for it, he can only read
        # If the user is creating a new reserve or trying to edit a form he has permission, he can change the fields accordingly
        readOnly = False
        if 'instance' in kwargs:
            if kwargs['instance']:
                reservable = kwargs['instance'].locavel
                if self.request.user not in reservable.responsavel.all():
                    readOnly = True

        if readOnly and not self.request.user.is_superuser:
            self.init_read_only(kwargs)
        else:
            self.init_status_field(kwargs)
            self.init_date_field()
            self.init_hour_fields()
            self.init_reservable_field(kwargs)
            self.init_activity_field()
            self.init_user_field()

    def init_read_only(self, kwargs):
        # For all fields, put the readonly widget and makes sure the data can't be tempered
        self.fields['data'].widget = ReadOnlyWidget()
        self.fields['data'].disabled = True
        self.fields['horaInicio'].widget = ReadOnlyWidget()
        self.fields['horaInicio'].disabled = True
        self.fields['horaFim'].widget = ReadOnlyWidget()
        self.fields['horaFim'].disabled = True
        self.fields['locavel'].widget = ReadOnlyWidget(type(kwargs['instance'].locavel))
        self.fields['locavel'].disabled = True
        self.fields['atividade'].widget = ReadOnlyWidget(type(kwargs['instance'].atividade))
        self.fields['ramal'].widget = ReadOnlyWidget()
        self.fields['ramal'].disabled = True
        self.fields['finalidade'].widget = ReadOnlyWidget()
        self.fields['finalidade'].disabled = True

        # The hidden fields are hidded
        self.fields['estado'].label = ''
        self.fields['estado'].widget = forms.HiddenInput()
        self.fields['usuario'].widget = forms.HiddenInput()
        self.fields['usuario'].label = ''


    def init_status_field(self, kwargs):
        # If we're creating a new form it's okay to hide the status.
        # If we're additing an existing one, it must show status if user is reponsable
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
        else:
            hide = True
        if hide and not self.request.user.is_superuser:
            self.fields['estado'].initial = 'E'
            self.fields['estado'].label = ''
            self.fields['estado'].widget = forms.HiddenInput()

    def init_user_field(self):
        # Hide if it's not superuser, otherwise check for errors and initialize
        if not self.request.user.is_superuser:
            self.fields['usuario'].initial = self.request.user
            self.fields['usuario'].widget = forms.HiddenInput()
            self.fields['usuario'].label = ''
        else:
            attrs = {}
            if 'usuario' in self.errors:
                attrs['error'] = self.errors['usuario']
            self.fields['usuario'].widget = AutocompleteWidget(attrs=attrs, query=User.objects.all(), model=User)

    def init_activity_field(self):
        # If there's a initial reservable get activities that belong to it
        if self.fields['locavel'].initial:
            reservable = self.reservable_type.objects.get(id=self.fields['locavel'].initial)
            self.fields['atividade'].queryset = reservable.atividadesPermitidas

        # Initialize the widget that dynamically change activities according to the selected reservable
        rel = Reserva._meta.get_field('atividade').rel
        self.fields['atividade'].widget = DynamicAtividadeWidget(Select(choices=models.ModelChoiceIterator(self.fields['atividade'])), rel, admin.admin.site, can_change_related=True)

    def init_reservable_field(self, kwargs):
        # If there was a error of validation there's the need to recover the reservable as pre-selected
        if self.errors:
            try:
                self.request.session['id_reservable'] = self.request.session['id_reservable_backup']
            except:
                pass

        # Check if there is a pre-selected reservable
        try:
            self.id_reservable = self.request.session['id_reservable']
        except:
            self.id_reservable = None

        # If user is changing an existing reserve the reserve's reservable already selected is the only option
        # If user is creating a reserve, the queryset of possible reservables is determinet
        if 'instance' in kwargs:
            if kwargs['instance']:
                reservable = kwargs['instance'].locavel
                queryset = self.reservable_type.objects.filter(id=reservable.id)
            else:
                ma = self.admin_type(self.reservable_type, AdminSite())
                queryset = ma.get_queryset(self.request)
        else:
            ma = self.admin_type(self.reservable_type, AdminSite())
            queryset = ma.get_queryset(self.request)

        # If there's a pre=selected reservable he is the option
        # Else the options are the user's queryset
        if self.id_reservable:
            self.fields['locavel'].initial = self.id_reservable
            self.fields['locavel'].queryset = self.reservable_type.objects.filter(id=self.id_reservable)
        else:
            self.fields['locavel'].queryset = queryset

            # id_reservable is saved so it can be recovered in case of validation error
        self.request.session['id_reservable_backup'] = self.id_reservable
        self.request.session['id_reservable'] = None

    def init_hour_fields(self):
        # Check fields for error and intialize Widgets
        attrs = {}
        if 'horaInicio' in self.errors:
            attrs['error'] = self.errors['horaInicio']
        self.fields['horaInicio'] = forms.TimeField(input_formats=['%H:%M'], widget=SelectTimeWidget(attrs=attrs))
        attrs = {}
        if 'horaFim' in self.errors:
            attrs['error'] = self.errors['horaFim']
        self.fields['horaFim'] = forms.TimeField(input_formats=['%H:%M'], widget=SelectTimeWidget(attrs=attrs))

        # See if there's a initial value
        try:
            self.fields['horaInicio'].initial = self.request.session['horaInicio']
            self.fields['horaFim'].initial = self.request.session['horaFim']
        except:
            pass
        self.request.session['horaInicio'] = ''
        self.request.session['horaFim'] = ''

    def init_date_field(self):
        # See if there's a initial value
        try:
            self.fields['data'].initial = self.request.session['data']
        except:
            pass
        self.request.session['data'] = ''

    def send_mail(self, status, instance):
        user = instance.usuario
        status = instance.estado
        reservable = instance.locavel
        date = instance.data
        start = instance.horaInicio
        end = instance.horaFim
        responsables = reservable.responsavel.all()
        # First we send an email to the user who asked for the reserve
        if status == 'A':
            email_title = 'Reserva de %s confirmada.' % reservable.nome.encode("utf-8")
            email_text = '''
                Olá, %s,
                Sua reserva de %s para o dia %s, das %s às %s, foi confirmada.

                -------
                E-mail automático, por favor não responda.
            ''' % (user, reservable.nome.encode("utf-8"), date.strftime('%d/%m/%Y'), start.strftime('%H:%M'), end.strftime('%H:%M'))
        elif status == 'E':
            email_title = 'Reserva de %s aguardando aprovação.' % reservable.nome.encode("utf-8")
            email_text = '''
                Olá, %s,
                Sua reserva de %s para o dia %s, das %s às %s, está aguardando aprovação. Você receberá uma notificação quando o estado da sua reserva for atualizado.

                -------
                E-mail automático, por favor não responda.
            ''' % (user, reservable.nome.encode("utf-8"), date.strftime('%d/%m/%Y'), start.strftime('%H:%M'), end.strftime('%H:%M'))
        elif status == 'D':
            email_title = 'Reserva de %s negada.' % reservable.nome.encode("utf-8")
            email_text = '''
                Olá, %s,
                Sua reserva de %s para o dia %s, das %s às %s, foi negada.

                -------
                E-mail automático, por favor não responda.
            ''' % (user, reservable.nome.encode("utf-8"), date.strftime('%d/%m/%Y'), start.strftime('%H:%M'), end.strftime('%H:%M'))
        send_mail(email_title, email_text, 'reservas.ccs@sistemas.ufsc.br', [user.email])

        # If the user doesn't have permission we need to send a e-mail to the reservable responsable
        if status == 'E':
            # Need to check reservable instance to genereate the link
            if isinstance(reservable, EspacoFisico):
                reserve_type = 'reservaespacofisico'
            elif isinstance(reservable, Equipamento):
                reserve_type = 'reservaequipamento'

            base_url = self.request.build_absolute_uri('/')
            url = "%sadmin/agenda/%s/%d/change/" % (base_url, reserve_type, instance.id)

            for responsable in responsables:
                email_title = 'Pedido de reserva de %s' % reservable.nome.encode("utf-8")
                email_text = '''
                    Olá, %s,
                    %s fez um pedido de reserva em %s, para o dia %s, das %s às %s. Use o link abaixo para analisar o pedido.
                    %s

                    -------
                    E-mail automático, por favor não responda.
                ''' % (responsable, user, reservable.nome.encode("utf-8"), date.strftime('%d/%m/%Y'), start.strftime('%H:%M'), end.strftime('%H:%M'), url)
                send_mail(email_title, email_text, 'reservas.ccs@sistemas.ufsc.br', [responsable.email])

    def save(self, *args, **kwargs):
        user_query = kwargs.pop('query', None)
        reservable = self.cleaned_data['locavel']
        status = self.cleaned_data['estado']
        instance = super(ReservaAdminForm, self).save(commit=False)

        # Check if the user has permission in this reservable
        # If it is, the reserve is automatically accepted
        if reservable in user_query:
            status = 'A'
        instance.estado = status
        instance.save()
        self.send_mail(status, instance)
        return instance

class ReservaEquipamentoAdminForm(ReservaAdminForm):
    class Meta:
        model = ReservaEquipamento
        fields = ('estado', 'data', 'horaInicio', 'horaFim', 'locavel', 'atividade', 'usuario', 'ramal', 'finalidade')
    def __init__(self, *args, **kwargs):
        kwargs['admin_type'] = admin.EquipamentoAdmin
        kwargs['reservable_type'] = Equipamento
        super(ReservaEquipamentoAdminForm, self).__init__(*args, **kwargs)

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
        kwargs['admin_type'] = admin.EspacoFisicoAdmin
        kwargs['reservable_type'] = EspacoFisico
        super(ReservaEspacoFisicoAdminForm, self).__init__(*args, **kwargs)

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
