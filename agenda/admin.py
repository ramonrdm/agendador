from django.contrib import admin
from agenda.models import *
from django.contrib.auth.models import User
from django.forms import HiddenInput
from django.contrib.admin.sites import AdminSite
import forms

admin.site.register(Atividade)
#admin.site.register(EspacoFisico)
#admin.site.register(Equipamento)

@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">account_balance</i>'


    def search_children(self, units, unit):
        children = Unidade.objects.filter(unidadePai=unit)
        for child in children:
            if child.nome == unit.nome:
                children = children.exclude(nome=unit.nome)
        if children:
            for child in children:
                units = self.search_children(units, child)
        else:
            units = units | unit
            return units
        return units

    def get_queryset(self, request):
        qs = super(UnidadeAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        units = Unidade.objects.none()
        unit_responsible = Unidade.objects.filter(responsavel=request.user)
        for unit in unit_responsible:
            units = self.search_children(units, unit)
        units = units.distinct()
        return units

    def get_readonly_fields(self, request, obj=None):
        qs = super(UnidadeAdmin, self).get_queryset(request)
        qsResp = qs.filter(responsavel=request.user)
        if request.user.is_superuser:
            return []
        if obj in qsResp:
            return ['responsavel']
        return []


class ReservaEquipamentoAdmin(admin.ModelAdmin):
    form = forms.ReservaEquipamentoAdminForm
    list_display = ('usuario', 'locavel', 'data', 'ramal', 'finalidade')
    search_fields = ['finalidade', 'usuario__username']
    icon = '<i class="material-icons">power</i>'

    def get_form(self, request, obj=None, **kwargs):
        AdminForm =  super(ReservaEquipamentoAdmin, self).get_form(request, obj, **kwargs)
        class AdminFormWithRequest(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)

        return AdminFormWithRequest

    def search_children(self, reserves, unit):
        children = Unidade.objects.filter(unidadePai=unit)
        for child in children:
            if child.nome == unit.nome:
                children = children.exclude(nome=unit.nome)
        if children:
            for child in children:
                reserves = self.search_children(reserves, child)
        else:
            equipments = Equipamento.objects.filter(unidade = unit)
            for equipment in equipments:
                reserves = reserves | ReservaEquipamento.objects.filter(locavel=equipment)
            return reserves
        equipments = Equipamento.objects.filter(unidade=unit)
        for equipment in equipments:
            reserves = reserves | ReservaEquipamento.objects.filter(locavel=equipment)
        return reserves

    def get_queryset(self, request):
        qs = super(ReservaEquipamentoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        reserves = ReservaEquipamento.objects.none()
        #Check if unit responsible
        unit_responsible = Unidade.objects.filter(responsavel=request.user)
        if unit_responsible:
            reservable = Equipamento.objects.filter(unidade=unit_responsible)
            reserves = reserves | ReservaEquipamento.objects.filter(locavel=reservable)
            #Check for children unit
            for unit in unit_responsible:
                reserves = self.search_children(reserves, unit)
#               item = Equipamento.objects.filter(unidade=child)
#               for item_child in item:
#                   reserves = reserves | item_child.reservalocavel_set.all()
        #Check if room responsible
        item_responsible = Equipamento.objects.filter(responsavel=request.user)
        if item_responsible:
            reserves = reserves | ReservaEquipamento.objects.filter(locavel=item_responsible)

        #Add own reserves
        reserves = reserves | ReservaEquipamento.objects.filter(usuario=request.user)

        reserves = reserves.distinct()
        return reserves


    # def get_form(self, request, obj=None, **kwargs):
    #   form = super(ReservaEquipamentoAdmin, self).get_form(request, obj, **kwargs)
    #   if 'id_equip' in request.session:
    #       form.base_fields['usuario'].initial = request.user.id
    #       form.base_fields['data'].initial = request.session['data']
    #       form.base_fields['locavel'].initial = request.session['id_equip']

    #   if not request.user.is_superuser:
    #       form.base_fields['usuario'].widget = HiddenInput()
    #       form.base_fields['usuario'].label = ""

    #   return form


    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #   if db_field.name == "usuario":
    #       if request.user.is_superuser:
    #           kwargs["queryset"] = User.objects.all()
    #       else:
    #           kwargs["queryset"] = User.objects.filter(id=request.user.id)
    #   if db_field.name == "locavel":
    #       if request.user.is_superuser:
    #           kwargs["queryset"] = Equipamento.objects.all()
    #       else:
    #           kwargs["queryset"] = Equipamento.objects.filter(id=request.session['id_equip'])
    #   return super(ReservaEquipamentoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(ReservaEquipamento, ReservaEquipamentoAdmin)

class ReservaEspacoFisicoAdmin(admin.ModelAdmin):
    form = forms.ReservaEspacoFisicoAdminForm
    list_display = ('usuario', 'locavel', 'data', 'ramal', 'finalidade')
    search_fields = ['finalidade', 'usuario__username']
    icon = '<i class="material-icons">room</i>'

    def get_form(self, request, obj=None, **kwargs):
        AdminForm =  super(ReservaEspacoFisicoAdmin, self).get_form(request, obj, **kwargs)
        class AdminFormWithRequest(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)

        return AdminFormWithRequest

    def search_children(self, reserves, unit):
        children = Unidade.objects.filter(unidadePai=unit)
        for child in children:
            if child.nome == unit.nome:
                children = children.exclude(nome=unit.nome)
        if children:
            for child in children:
                reserves = self.search_children(reserves, child)
        else:
            places = EspacoFisico.objects.filter(unidade = unit)
            for place in places:
                reserves = reserves | ReservaEspacoFisico.objects.filter(locavel=place)
            return reserves
        places = EspacoFisico.objects.filter(unidade = unit)
        for place in places:
            reserves = reserves | ReservaEspacoFisico.objects.filter(locavel=place)
        return reserves


    def get_queryset(self, request):
        qs = super(ReservaEspacoFisicoAdmin, self).get_queryset(request)
        # Super user case
        if request.user.is_superuser:
            return qs

        reserves = ReservaEspacoFisico.objects.none()
        # Check if unit responsible
        unit_responsible = Unidade.objects.filter(responsavel=request.user)
        if unit_responsible:
            reservable = EspacoFisico.objects.filter(unidade=unit_responsible)
            reserves = reserves | ReservaEspacoFisico.objects.filter(locavel=reservable)
            # Check for children unit
            for unit in unit_responsible:       
                reserves = self.search_children(reserves, unit)
                
#           children = Unidade.objects.filter(unidadePai=unit_responsible)
#           for child in children:
#               room = EspacoFisico.objects.filter(unidade=child)
#               for room_child in room:
#                   reserves = reserves | room_child.reservaespacofisico_set.all()

        # Check if room responsible
        room_responsible = EspacoFisico.objects.filter(responsavel=request.user)
        if room_responsible:
            reserves = reserves | ReservaEspacoFisico.objects.filter(locavel=room_responsible)

        #Add own reserves
        reserves = reserves | ReservaEspacoFisico.objects.filter(usuario=request.user)

        reserves = reserves.distinct()
        return reserves

admin.site.register(ReservaEspacoFisico, ReservaEspacoFisicoAdmin)

class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('nome','unidade','get_responsavel')
    def get_responsavel(self, obj):
        return ", ".join(responsavel.username for responsavel in obj.responsavel.all())
    get_responsavel.short_description = 'responsavel'

    def add_equipment(self, user, unit, equipment, equipments, responsable):
        group = equipment.grupo
        if not group and unit not in user.unidade_set.all() and not responsable:
            equipments = equipments | Equipamento.objects.filter(id=equipment.id).exclude(visivel=False)
        elif unit in user.unidade_set.all() or responsable:
            equipments = equipments | Equipamento.objects.filter(id=equipment.id)
        return equipments

    def search_children(self, equipments, unit, user, responsable):
        children = Unidade.objects.filter(unidadePai=unit)
        for child in children:
            if child.nome == unit.nome:
                children = children.exclude(nome=unit.nome)
        if children:
            for child in children:
                equipments = self.search_children(equipments, child, user, responsable)
        else:
            child_equipments = Equipamento.objects.filter(unidade=unit)
            ## Test if equipment isn't bound to a specific group
            for equipment in child_equipments:
                equipments = self.add_equipment(user, unit, equipment, equipments, responsable)
            return equipments
        # You may also have a son AND equipments, this equipment may also belong to a group
        unit_equipments = Equipamento.objects.filter(unidade=unit)
        for equipment in unit_equipments:
            equipments = self.add_equipment(user, unit, equipment, equipments, responsable)
        return equipments

    def get_queryset(self, request):
        qs = super(EquipamentoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        equipments = Equipamento.objects.none()
        # Check if unit responsible
        # Also check user unit via group, for form list purposes
        groups = request.user.groups.all()
        group_units = Unidade.objects.none()
        for group in groups:
            if group.unidade_set:
                group_units = group_units | group.unidade_set.all()
        if group_units:
            for unit in group_units:
                equipments = self.search_children(equipments, unit, request.user, False)

        unit_responsible = Unidade.objects.filter(responsavel=request.user)
        if unit_responsible:
            for unit in unit_responsible:
                equipments = self.search_children(equipments, unit, request.user, True)

        # Get all equipments user's responsible
        equipments = equipments | Equipamento.objects.filter(responsavel=request.user)
        # Unit via group already tested, now test group exclusive spaces
        groups = request.user.groups.all()
        for group in groups:
            equipments = equipments | group.equipamento_set.all()
        equipments = equipments.distinct()
        return equipments

    def get_readonly_fields(self, request, obj=None):
        qs = super(EquipamentoAdmin, self).get_queryset(request)
        qsResp = qs.filter(responsavel=request.user)
        if request.user.is_superuser:
            return []
        else:
            return ['get_responsavel', 'unidade']


admin.site.register(Equipamento, EquipamentoAdmin)

class EspacoFisicoAdmin(admin.ModelAdmin):
    list_display = ('nome','unidade','get_responsavel')

    def get_responsavel(self, obj):
        return ", ".join([responsavel.username for responsavel in obj.responsavel.all()])
    get_responsavel.short_description = 'responsavel'

    def add_space(self, user, unit, space, spaces, responsable):
        group = space.grupo
        if not group and unit not in user.unidade_set.all() and not responsable:
            spaces = spaces | EspacoFisico.objects.filter(id=space.id).exclude(visivel=False)
        elif unit in user.unidade_set.all() or responsable:
            spaces = spaces | EspacoFisico.objects.filter(id=space.id)
        return spaces

    def search_children(self, spaces, unit, user, responsable):
        children = Unidade.objects.filter(unidadePai=unit)
        for child in children:
            if child.nome == unit.nome:
                children = children.exclude(nome=unit.nome)
        if children:
            for child in children:
                spaces = self.search_children(spaces, child, user, responsable)
        else:
            child_spaces = EspacoFisico.objects.filter(unidade=unit)
            ## Test if place isn't bound to a specific group
            for space in child_spaces:
                spaces = self.add_space(user, unit, space, spaces, responsable)
            return spaces
        # You may also have a child AND spacaces, this space may also belong to a group
        unit_spaces = EspacoFisico.objects.filter(unidade=unit)
        for space in unit_spaces:
            spaces = self.add_space(user, unit, space, spaces, responsable)
        return spaces

    def get_queryset(self, request):
        qs = super(EspacoFisicoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        spaces = EspacoFisico.objects.none()
        # Also check user unit via group, for form list purposes
        groups = request.user.groups.all()
        group_units = Unidade.objects.none()
        for group in groups:
            if group.unidade_set:
                group_units = group_units | group.unidade_set.all()
        if group_units:
            for unit in group_units:
                spaces = self.search_children(spaces, unit, request.user, False)

        # Check if unit responsible. 
        unit_responsible = Unidade.objects.filter(responsavel=request.user)
        if unit_responsible:
            for unit in unit_responsible:
                spaces = self.search_children(spaces, unit, request.user, True)
        # Get all spaces user's responsible
        spaces = spaces | EspacoFisico.objects.filter(responsavel=request.user)

        # Unit via group already tested, now test group exclusive spaces
        groups = request.user.groups.all()
        for group in groups:
            spaces = spaces | group.espacofisico_set.all()
        spaces = spaces.distinct()
        return spaces

    def get_readonly_fields(self, request, obj=None):
        qs = super(EspacoFisicoAdmin, self).get_queryset(request)
        qsResp = qs.filter(responsavel=request.user)
        if request.user.is_superuser:
            return []
        if obj in qsResp:
            return ['get_responsavel', 'unidade']
        return []

admin.site.register(EspacoFisico, EspacoFisicoAdmin)