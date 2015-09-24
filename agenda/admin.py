from django.contrib import admin
from models import *

admin.site.register(Evento)
admin.site.register(EspacoFisico)
admin.site.register(Equipamento)
admin.site.register(Grupo)

class ReservaEquipamentoAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'espacoFisico', 'data', 'ramal', 'finalidade')
	search_fields = ['finalidade', 'usuario__username']
admin.site.register(ReservaEquipamento, ReservaEquipamentoAdmin)

class ReservaEspacoFisicoAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'espacoFisico', 'data', 'ramal', 'finalidade')
	search_fields = ['finalidade', 'usuario__username']
admin.site.register(ReservaEspacoFisico, ReservaEspacoFisicoAdmin)