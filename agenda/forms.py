# -*- coding: utf-8 -*-

from agenda.models import Reserva
from django import forms
from django.contrib.admin import widgets
import datetime
from django.core.mail import send_mail
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm, Form


class FormReserva(forms.ModelForm):
	"""Formulário de reservas CCS"""
	dataReserva = forms.DateTimeField(initial=datetime.datetime.now)
	class Meta:
		model = Reserva
	#horaInicio = forms.DateTimeField(label="Data Inicio: (24:59)", initial="24:59")
	def __init__(self, *args, **kwargs):
		super(FormReserva, self).__init__(*args, **kwargs)
		self.fields['data'].widget = widgets.AdminDateWidget()
		self.fields['horaInicio'].widget = widgets.AdminTimeWidget()
		self.fields['horaInicio'].initial = "24:00"
		self.fields['horaFim'].widget = widgets.AdminTimeWidget()



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

