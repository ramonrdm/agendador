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