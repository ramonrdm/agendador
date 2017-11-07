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
		super(ReservaAdminForm, self).__init__(*args, **kwargs)


class ReservaEquipamentoAdminForm(ReservaAdminForm):
	"""docstring for ReservaEquipamentoAdminForm"""
	class Meta:
		model = ReservaEquipamento
		fields = '__all__'
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop("request", None)
		super(ReservaEquipamentoAdminForm, self).__init__(*args, **kwargs)
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
		self.request = kwargs.pop("request", None)
		super(ReservaEspacoFisicoAdminForm, self).__init__(*args, **kwargs)

				
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
