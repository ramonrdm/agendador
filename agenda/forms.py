# -*- coding: utf-8 -*-
from django import forms
from models import Reserva

class FormReserva(forms.ModelForm):
	"""Formulário de reservas CCS"""
	class meta:
		model = Reserva