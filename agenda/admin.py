from django.contrib import admin
from agenda.models import *
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
	list_display = ('usuario', 'espacoFisico', 'data', 'ramal', 'finalidade')
	search_fields = ['finalidade', 'usuario__username']
	icon = '<i class="material-icons">power</i>'

	def get_form(self, request, obj=None, **kwargs):
		form = super(ReservaEquipamentoAdmin, self).get_form(request, obj, **kwargs)
		if 'id_equip' in request.session:
			form.base_fields['usuario'].initial = request.user.id
			form.base_fields['data'].initial = request.session['data']
			form.base_fields['espacoFisico'].initial = request.session['id_equip']

		if not request.user.is_superuser:
			form.base_fields['usuario'].widget = HiddenInput()
			form.base_fields['usuario'].label = ""

		return form


	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "usuario":
			if request.user.is_superuser:
				kwargs["queryset"] = User.objects.all()
			else:
				kwargs["queryset"] = User.objects.filter(id=request.user.id)
		if db_field.name == "espacoFisico":
			if request.user.is_superuser:
				kwargs["queryset"] = Equipamento.objects.all()
			else:
				kwargs["queryset"] = Equipamento.objects.filter(id=request.session['id_equip'])
		return super(ReservaEquipamentoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(ReservaEquipamento, ReservaEquipamentoAdmin)

class ReservaEspacoFisicoAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'espacoFisico', 'data', 'ramal', 'finalidade')
	search_fields = ['finalidade', 'usuario__username']
	icon = '<i class="material-icons">room</i>'
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