from django.contrib import admin
from models import *

admin.site.register(EspacoFisico)
admin.site.register(TipoEvento)
admin.site.register(Equipamento)
admin.site.register(Grupo)

class ReservaAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'espacoFisico', 'data', 'ramal', 'finalidade')
	search_fields = ['finalidade', 'usuario__username']
admin.site.register(Reserva, ReservaAdmin)