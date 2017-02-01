from django.contrib import admin
from agenda.models import *

admin.site.register(Evento)
admin.site.register(EspacoFisico)
admin.site.register(Equipamento)
#admin.site.register(Grupo)

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
	icon = '<i class="material-icons">group</i>'

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