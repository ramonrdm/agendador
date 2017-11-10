# -*- coding: utf-8 -*-

from agenda.models import Reserva, EspacoFisico, ReservaEspacoFisico, ReservaEquipamento, Equipamento
from django import forms
from django.contrib.admin import widgets
import datetime
from django.core.mail import send_mail
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm, Form, HiddenInput
from django.contrib.admin.sites import AdminSite
from django.core.exceptions import ValidationError
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
        if not self.request.user.is_superuser:
            self.fields['usuario'].initial = self.request.user
            self.fields['usuario'].disabled
            self.fields['usuario'].widget = forms.HiddenInput()
            self.fields['usuario'].label = ''

class ReservaEquipamentoAdminForm(ReservaAdminForm):
    """docstring for ReservaEquipamentoAdminForm"""
    class Meta:
        model = ReservaEquipamento
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(ReservaEquipamentoAdminForm, self).__init__(*args, **kwargs)
        ma = admin.EquipamentoAdmin(Equipamento, AdminSite())
        queryset = ma.get_queryset(self.request).exclude(visivel=False)
        self.fields['equipamento'].queryset = queryset
        try:
            self.fields['equipamento'].initial = self.request.session['id_equip']
        except:
            pass

class ReservaEspacoFisicoAdminForm(ReservaAdminForm):
    """Formulário de reservas CCS"""
    #dataReserva = forms.DateTimeField(initial=datetime.datetime.now)
    class Meta:
        model = ReservaEspacoFisico
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(ReservaEspacoFisicoAdminForm, self).__init__(*args, **kwargs)
        ma = admin.EspacoFisicoAdmin(EspacoFisico, AdminSite())
        queryset = ma.get_queryset(self.request).exclude(visivel=False)
        self.fields['espacoFisico'].queryset = queryset
        try:
            self.fields['espacoFisico'].initial = self.request.session['id_equip']
        except:
            pass
                
        #espacoatual = args.pop("espacoatual")
        #print "bluh"
        #print espacoatual
        #espacoatual = EspacoFisico.objects.filter(id=6)
        #self.fields['espacoFisico'] = espacoatual
        #form.fields['evento'].queryset = espacoatual[0].eventosPermitidos

    def clean(self):
        self.choque()
        self.bloqueado()

    def bloqueado(self):
        if self.cleaned_data['espacoFisico'].bloqueado:
            raise ValidationError({'espacoFisico': 'Espaço físico bloqueado'})

    def choque(self):
        reservas = ReservaEspacoFisico.objects.filter(espacoFisico=self.cleaned_data['espacoFisico'], data=self.cleaned_data['data'])
        for r in reservas:
            if  (
                (self.cleaned_data['horaFim']  > r.horaInicio and self.cleaned_data['horaFim'] < r.horaFim) or 
                (self.cleaned_data['horaInicio'] > r.horaInicio and self.cleaned_data['horaInicio'] < r.horaFim ) or 
                (self.cleaned_data['horaInicio'] == r.horaInicio and self.cleaned_data['horaFim'] == r.horaFim) or
                (r.horaInicio > self.cleaned_data['horaInicio'] and r.horaInicio < self.cleaned_data['horaFim']) or
                (self.cleaned_data['horaInicio'] < r.horaFim < self.cleaned_data['horaFim'])
                ):
                raise ValidationError({'data': 'choque!'})
        
    def enviarEmail(self, mail):
        mensagem_email="Reserva de espaço físico "+str(self.cleaned_data['horaInicio'])+'/'+str(self.cleaned_data['horaFim'])+' '+str(self.cleaned_data['data'])+' - '+str(self.cleaned_data['espacoFisico'])+", realizada com sucesso"
        send_mail('Reserva CCS - '+str(self.cleaned_data['espacoFisico'])+' - '+str(self.cleaned_data['data']), mensagem_email, 'reservas.ccs@sistemas.ufsc.br', [mail], fail_silently=False)
