# -*- coding: utf-8 -*-

from agenda.models import Reserva
from django import forms
from django.contrib.admin import widgets
import datetime


class FormReserva(forms.ModelForm):
	"""Formulário de reservas CCS"""
	#horaInicio = forms.DateTimeField(widget=DateTimeWidget(format= '%d/%m/%Y %H:%M',input_formats=['%d/%m/%Y %H:%M']))
	#horaFim = forms.DateTimeField()
	#horaInicio = forms.DateTimeField(initial=datetime.datetime.now())
	#horaInicio = forms.DateTimeField(widget = widgets.AdminSplitDateTime())
	#dataa = datetime.datetime.now()
	#dataa = dataa.strftime('%Y/%m/%d %H:%M')
	#print dataa
	#horaInicio = forms.SplitDateTimeField(initial=datetime.datetime.now, input_time_formats=['%H:%M'])
	#horaInicio = forms.SplitDateTimeField(input_time_formats=['%H:%M'], label='Data e hora inicial')
	#horaFim = forms.SplitDateTimeField(initial=datetime.datetime.now, label='Data e hora final')
	#dataReserva = forms.SplitDateTimeField(initial=datetime.datetime.now)
	dataReserva = forms.DateTimeField(initial=datetime.datetime.now)
	class Meta:
		model = Reserva
		#exclude = ['estado']
	#def __init__(self, *args, **kwargs):
		#super(FormReserva, self).__init__(*args, **kwargs)
		#self.fields['horaInicio'].widget = widgets.AdminSplitDateTime()
		#self.fields['horaInicio'].widget = widgets.AdminDateWidget()
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
		
#	def maisUmDia(self):
#		"""verifica se está agendadno para somente um dia"""
#		if self.cleaned_data['horaInicio'].strftime("%Y-%m-%d") == self.cleaned_data['horaFim'].strftime("%Y-%m-%d"):
#			return False
#		else:
#			return True
