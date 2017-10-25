from django.contrib import admin
from agenda.models import *
from agenda.forms import ReservaEquipamentoAdminForm
from django.contrib.auth.models import User
from django.forms import HiddenInput

admin.site.register(Atividade)
#admin.site.register(EspacoFisico)
#admin.site.register(Equipamento)

@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
	icon = '<i class="material-icons">group</i>'

	def get_queryset(self, request):
		qs = super(UnidadeAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(responsavel=request.user)

	def get_readonly_fields(self, request, obj=None):
		qs = super(UnidadeAdmin, self).get_queryset(request)
		qsResp = qs.filter(responsavel=request.user)
		if request.user.is_superuser:
			return []
		if obj in qsResp:
			return ['responsavel']
		return []


class ReservaEquipamentoAdmin(admin.ModelAdmin):
	form = ReservaEquipamentoAdminForm
	list_display = ('usuario', 'equipamento', 'data', 'ramal', 'finalidade')
	search_fields = ['finalidade', 'usuario__username']
	icon = '<i class="material-icons">power</i>'

	def get_form(self, request, obj=None, **kwargs):
		AdminForm =  super(ReservaEquipamentoAdmin, self).get_form(request, obj, **kwargs)
		class AdminFormWithRequest(AdminForm):
			def __new__(cls, *args, **kwargs):
				kwargs['request'] = request
				return AdminForm(*args, **kwargs)

		return AdminFormWithRequest

	def get_queryset(self, request):
		qs = super(ReservaEquipamentoAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs

		reserves = ReservaEquipamento.objects.none()
		#Check if unity responsible
		unity_responsible = Unidade.objects.filter(responsavel=request.user)
		if unity_responsible:
			reservable = Equipamento.objects.filter(unidade=unity_responsible)
			for item in reservable:
				reseves = reserves | ReservaEquipamento.objects.filter(equipamento=item)
			#Check for children unity
			children = Unidade.objects.filter(unidadePai=unity_responsible)
			if children:
				for child in children:
					item = Equipamento.objects.filter(unidade=child)
					if item:
						for item_child in item:
							reserves = reserves | place_child.reservaequipamento_set.all()

		#Check if place responsible
		item_responsible = Equipamento.objects.filter(responsavel=request.user)
		if item_responsible:
			reserves = reserves | ReservaEquipamento.objects.filter(equipamento=item_responsible)

		#Add own reserves
		reserves = reserves | ReservaEquipamento.objects.filter(usuario=request.user)

		return reserves


	# def get_form(self, request, obj=None, **kwargs):
	# 	form = super(ReservaEquipamentoAdmin, self).get_form(request, obj, **kwargs)
	# 	if 'id_equip' in request.session:
	# 		form.base_fields['usuario'].initial = request.user.id
	# 		form.base_fields['data'].initial = request.session['data']
	# 		form.base_fields['espacoFisico'].initial = request.session['id_equip']

	# 	if not request.user.is_superuser:
	# 		form.base_fields['usuario'].widget = HiddenInput()
	# 		form.base_fields['usuario'].label = ""

	# 	return form


	# def formfield_for_foreignkey(self, db_field, request, **kwargs):
	# 	if db_field.name == "usuario":
	# 		if request.user.is_superuser:
	# 			kwargs["queryset"] = User.objects.all()
	# 		else:
	# 			kwargs["queryset"] = User.objects.filter(id=request.user.id)
	# 	if db_field.name == "espacoFisico":
	# 		if request.user.is_superuser:
	# 			kwargs["queryset"] = Equipamento.objects.all()
	# 		else:
	# 			kwargs["queryset"] = Equipamento.objects.filter(id=request.session['id_equip'])
	# 	return super(ReservaEquipamentoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(ReservaEquipamento, ReservaEquipamentoAdmin)

class ReservaEspacoFisicoAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'espacoFisico', 'data', 'ramal', 'finalidade')
	search_fields = ['finalidade', 'usuario__username']
	icon = '<i class="material-icons">room</i>'

	def get_queryset(self, request):
		qs = super(ReservaEspacoFisicoAdmin, self).get_queryset(request)
		# Super user case
		if request.user.is_superuser:
			return qs

		reserves = ReservaEspacoFisico.objects.none()
		#Check if unity responsible
		unity_responsible = Unidade.objects.filter(responsavel=request.user)
		if unity_responsible:
			reservable = EspacoFisico.objects.filter(unidade=unity_responsible)
			for place in reservable:
				reseves = reserves | ReservaEspacoFisico.objects.filter(espacoFisico=place)
			#Check for children unity
			children = Unidade.objects.filter(unidadePai=unity_responsible)
			if children:
				for child in children:
					place = EspacoFisico.objects.filter(unidade=child)
					if place:
						for place_child in place:
							reserves = reserves | place_child.reservaespacofisico_set.all()

		#Check if place responsible
		place_responsible = EspacoFisico.objects.filter(responsavel=request.user)
		if place_responsible:
			reserves = reserves | ReservaEspacoFisico.objects.filter(espacoFisico=place_responsible)

		#Add own reserves
		reserves = reserves | ReservaEspacoFisico.objects.filter(usuario=request.user)

		return reserves

admin.site.register(ReservaEspacoFisico, ReservaEspacoFisicoAdmin)

class EquipamentoAdmin(admin.ModelAdmin):
	list_display = ('nome','unidade','responsavel')

	def get_queryset(self, request):
		qs = super(EquipamentoAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(responsavel=request.user)

	def get_readonly_fields(self, request, obj=None):
		qs = super(EquipamentoAdmin, self).get_queryset(request)
		qsResp = qs.filter(responsavel=request.user)
		if request.user.is_superuser:
			return []
		else:
			return ['responsavel', 'unidade']


admin.site.register(Equipamento, EquipamentoAdmin)

class EspacoFisicoAdmin(admin.ModelAdmin):
	list_display = ('nome','unidade','responsavel')

	def get_queryset(self, request):
		qs = super(EspacoFisicoAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(responsavel=request.user)

	def get_readonly_fields(self, request, obj=None):
		qs = super(EspacoFisicoAdmin, self).get_queryset(request)
		qsResp = qs.filter(responsavel=request.user)
		if request.user.is_superuser:
			return []
		if obj in qsResp:
			return ['responsavel', 'unidade']
		return []

admin.site.register(EspacoFisico, EspacoFisicoAdmin)