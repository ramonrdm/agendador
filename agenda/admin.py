from django.contrib import admin
from agenda.models import *

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

class ReservaEquipamentoAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'espacoFisico', 'data', 'ramal', 'finalidade')
	search_fields = ['finalidade', 'usuario__username']
	icon = '<i class="material-icons">power</i>'

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

admin.site.register(Equipamento, EquipamentoAdmin)

class EspacoFisicoAdmin(admin.ModelAdmin):
	list_display = ('nome','unidade','responsavel')

	def get_queryset(self, request):
		qs = super(EspacoFisicoAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(responsavel=request.user)

admin.site.register(EspacoFisico, EspacoFisicoAdmin)	