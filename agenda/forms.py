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
	dataUsoInicio = forms.SplitDateTimeField(initial=datetime.datetime.now)
	dataUsoFim = forms.SplitDateTimeField(initial=datetime.datetime.now)
	dataReserva = forms.SplitDateTimeField(initial=datetime.datetime.now)
	class Meta:
		model = Reserva
		#exclude = ['estado', 'dataReserva', 'usuario']
	#def __init__(self, *args, **kwargs):
		#super(FormReserva, self).__init__(*args, **kwargs)
		#self.fields['dataUsoInicio'].widget = widgets.AdminSplitDateTime()
		#self.fields['dataUsoInicio'].widget = widgets.AdminDateWidget()