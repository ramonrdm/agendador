# -*- coding: utf-8 -*-

from agenda.models import Reserva, EspacoFisico, ReservaEspacoFisico, ReservaEquipamento, Equipamento
from django import forms
from django.contrib.admin import widgets
import datetime
from django.core.mail import send_mail
from django.forms import ModelForm, Form, HiddenInput
from django.contrib.admin.sites import AdminSite
from django.core.exceptions import ValidationError
from django.contrib.admin import widgets
from widgets import SelectTimeWidget, SelectDateWidget
from django.contrib.auth.models import User
import admin

class ReservaAdminForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(ReservaAdminForm, self).__init__(*args, **kwargs)
        try:
            self.fields['data'].initial = self.request.session['data']
        except:
            pass
        self.request.session['data'] = ''
        if not self.request.user.is_superuser:
            self.fields['usuario'].initial = self.request.user
            self.fields['usuario'].widget = forms.HiddenInput()
            self.fields['usuario'].label = ''
        self.fields['horaInicio'] = forms.TimeField(input_formats=['%H:%M'], widget=SelectTimeWidget())
        self.fields['horaFim'] = forms.TimeField(input_formats=['%H:%M'], widget=SelectTimeWidget())
        print self.fields['data'].widget

class ReservaEquipamentoAdminForm(ReservaAdminForm):
    class Meta:
        model = ReservaEquipamento
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(ReservaEquipamentoAdminForm, self).__init__(*args, **kwargs)
        try:
            self.id_equip = self.request.session['id_equip']
        except:
            self.id_equip = None
        if self.id_equip:
            self.fields['locavel'].initial = self.id_equip
            self.fields['locavel'].queryset = Equipamento.objects.filter(id=self.id_equip)
        else:
            ma = admin.EquipamentoAdmin(Equipamento, AdminSite())
            queryset = ma.get_queryset(self.request)
            self.fields['locavel'].queryset = queryset
        self.request.session['id_equip'] = None

class ReservaEspacoFisicoAdminForm(ReservaAdminForm):
    class Meta:
        model = ReservaEspacoFisico
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(ReservaEspacoFisicoAdminForm, self).__init__(*args, **kwargs)
        try:
            self.id_equip = self.request.session['id_equip']
        except:
            self.id_equip = None
        if self.id_equip:
            self.fields['locavel'].initial = self.id_equip
            self.fields['locavel'].queryset = EspacoFisico.objects.filter(id=self.id_equip)
        else:
            ma = admin.EspacoFisicoAdmin(EspacoFisico, AdminSite())
            queryset = ma.get_queryset(self.request)
            self.fields['locavel'].queryset = queryset
        self.request.session['id_equip'] = None
        
    def enviarEmail(self, mail):
        mensagem_email="Reserva de espaço físico "+str(self.cleaned_data['horaInicio'])+'/'+str(self.cleaned_data['horaFim'])+' '+str(self.cleaned_data['data'])+' - '+str(self.cleaned_data['espacoFisico'])+", realizada com sucesso"
        send_mail('Reserva CCS - '+str(self.cleaned_data['espacoFisico'])+' - '+str(self.cleaned_data['data']),
         mensagem_email,
         'reservas.ccs@sistemas.ufsc.br',
         [mail],
         fail_silently=False)

class SearchFilterForm(forms.Form):
    data = forms.DateField(input_formats=['%d/%m/%Y'], widget=SelectDateWidget())
    data.label = ''
    horaInicio = forms.TimeField(input_formats=['%H:%M'], widget=SelectTimeWidget())
    horaInicio.label = ''
    horaFim = forms.TimeField(input_formats=['%H:%M'], widget=SelectTimeWidget())
    horaFim.label = ''

    def clean(self):
        cleaned_data = super(SearchFilterForm, self).clean()
