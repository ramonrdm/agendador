# -*- coding: utf-8 -*-

from agenda.models import Reserva
from django import forms
from django.contrib.admin import widgets
import datetime


class FormReserva(forms.ModelForm):
	"""Formulário de reservas CCS"""
	#dataUsoInicio = forms.DateTimeField(widget=DateTimeWidget(format= '%d/%m/%Y %H:%M',input_formats=['%d/%m/%Y %H:%M']))
	#dataUsoFim = forms.DateTimeField()
	#dataUsoInicio = forms.DateTimeField(initial=datetime.datetime.now())
	#dataUsoInicio = forms.DateTimeField(widget = widgets.AdminSplitDateTime())
	#dataa = datetime.datetime.now()
	#dataa = dataa.strftime('%Y/%m/%d %H:%M')
	#print dataa
	#dataUsoInicio = forms.SplitDateTimeField(initial=datetime.datetime.now, input_time_formats=['%H:%M'])
	dataUsoInicio = forms.SplitDateTimeField(input_time_formats=['%H:%M'], label='Data e hora inicial')
	dataUsoFim = forms.SplitDateTimeField(initial=datetime.datetime.now, label='Data e hora final')
	#dataReserva = forms.SplitDateTimeField(initial=datetime.datetime.now)
	dataReserva = forms.DateTimeField(initial=datetime.datetime.now)
	class Meta:
		model = Reserva
		#exclude = ['estado']
	#def __init__(self, *args, **kwargs):
		#super(FormReserva, self).__init__(*args, **kwargs)
		#self.fields['dataUsoInicio'].widget = widgets.AdminSplitDateTime()
		#self.fields['dataUsoInicio'].widget = widgets.AdminDateWidget()
	def choque(self, p):
		print p.cleaned_data['dataUsoInicio']
		#reservas = Reserva.objects.filter(dataUsoInicio=p.fields['dataUsoInicio'], espacoFisico=p.fields['espacoFisico'], dataUsoInicio__month=month, dataUsoInicio__day=day)
		reservas = Reserva.objects.filter(espacoFisico=p.cleaned_data['espacoFisico'])
		for r in reservas:
			if  (
				(p.cleaned_data['dataUsoFim']  > r.dataUsoInicio and p.cleaned_data['dataUsoFim'] < r.dataUsoFim) or 
				(p.cleaned_data['dataUsoInicio'] > r.dataUsoInicio and p.cleaned_data['dataUsoInicio'] < r.dataUsoFim ) or 
				(p.cleaned_data['dataUsoInicio'] == r.dataUsoInicio and p.cleaned_data['dataUsoFim'] == r.dataUsoFim) or
				(r.dataUsoInicio > p.cleaned_data['dataUsoInicio'] and r.dataUsoInicio < p.cleaned_data['dataUsoFim']) or
				(p.cleaned_data['dataUsoInicio'] < r.dataUsoFim < p.cleaned_data['dataUsoFim'])
				):
				return True
		return False
		
	def maisUmDia(self):
		"""verifica se está agendadno para somente um dia"""
		print "data somente:"
		#print self.fields['dataUsoInicio'].date
		print self.cleaned_data['dataUsoInicio'].strftime("%Y-%m-%d")
		print self.cleaned_data['dataUsoFim'].strftime("%Y-%m-%d")
		#self.cleaned_data['dataUsoInicio'] == self.cleaned_data['dataUsoFim']
		if self.cleaned_data['dataUsoInicio'].strftime("%Y-%m-%d") == self.cleaned_data['dataUsoFim'].strftime("%Y-%m-%d"):
			return False
		else:
			return True
