from django.contrib import admin
from models import *
# Register your models here.

admin.site.register(Departamento)
admin.site.register(EspacoFisico)
admin.site.register(TipoEvento)
class ReservaAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'departamento', 'espacoFisico', 'data', 'ramal', 'finalidade')
	search_fields = ['finalidade', 'usuario__username']
admin.site.register(Reserva, ReservaAdmin)