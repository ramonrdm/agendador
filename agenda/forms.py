# -*- coding: utf-8 -*-

from agenda.models import Reserva, EspacoFisico, ReservaEspacoFisico, ReservaEquipamento
from django import forms
from django.contrib.admin import widgets
import datetime
from django.core.mail import send_mail
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm, Form, HiddenInput

class ReservaAdminForm(forms.ModelForm):
	class Meta:
		model = Reserva
		fields = '__all__'
	def __init__(self, *args, **kwargs):
		self.request = kwargs['request']
		super(ReservaAdminForm, self).__init__(*args, **kwargs)
		self.fields['usuario'].initial = self.request.user.id
		try:
			self.fields['data'].initial = self.request.session['data']
		except:
			pass
		if not self.request.user.is_superuser:
			self.fields['usuario'].widget = HiddenInput()
			self.fields['usuario'].label = ""

class ReservaEquipamentoAdminForm(ReservaAdminForm):
	"""docstring for ReservaEquipamentoAdminForm"""
	class Meta:
		model = ReservaEquipamento
		fields = '__all__'
	def __init__(self, *args, **kwargs):
		self.request = kwargs["request"]
		super(ReservaAdminForm, self).__init__(self.request)
		super(ReservaEquipamentoAdminForm, self).__init__(*args, **kwargs)
		self.fields['usuario'].initial = self.request.user.id
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
		self.request = kwargs["request"]
		super(ReservaAdminForm, self).__init__(self.request)
		super(ReservaEspacoFisicoAdminForm, self).__init__(*args, **kwargs)
		self.fields['data'].widget = widgets.AdminDateWidget()
		self.fields['horaInicio'].widget = widgets.AdminTimeWidget()
		#self.fields['horaInicio'].initial = "24:00"
		self.fields['horaFim'].widget = widgets.AdminTimeWidget()
		try:
			self.fields['espacoFisico'].initial = self.request.session['id_place']
		except:
			pass
				
		#espacoatual = args.pop("espacoatual")
		#print "bluh"
		#print espacoatual
		#espacoatual = EspacoFisico.objects.filter(id=6)
        #self.fields['espacoFisico'] = espacoatual
        #form.fields['evento'].queryset = espacoatual[0].eventosPermitidos


	def choque(self):
		reservas = Reserva.objects.filter(espacoFisico=self.cleaned_data['espacoFisico'], data=self.cleaned_data['data'])
		for r in reservas:
			if  (
				(self.cleaned_data['horaFim']  > r.horaInicio and self.cleaned_data['horaFim'] < r.horaFim) or 
				(self.cleaned_data['horaInicio'] > r.horaInicio and self.cleaned_data['horaInicio'] < r.horaFim ) or 
				(self.cleaned_data['horaInicio'] == r.horaInicio and self.cleaned_data['horaFim'] == r.horaFim) or
				(r.horaInicio > self.cleaned_data['horaInicio'] and r.horaInicio < self.cleaned_data['horaFim']) or
				(self.cleaned_data['horaInicio'] < r.horaFim < self.cleaned_data['horaFim'])
				):
				return True
		return False
		
	def enviarEmail(self, mail):
		mensagem_email="Reserva de espaço físico "+str(self.cleaned_data['horaInicio'])+'/'+str(self.cleaned_data['horaFim'])+' '+str(self.cleaned_data['data'])+' - '+str(self.cleaned_data['espacoFisico'])+", realizada com sucesso"
		send_mail('Reserva CCS - '+str(self.cleaned_data['espacoFisico'])+' - '+str(self.cleaned_data['data']), mensagem_email, 'reservas.ccs@sistemas.ufsc.br', [mail], fail_silently=False)

