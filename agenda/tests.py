# this whole file is a huge copy and paste. it needs a serious refactor

from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.contrib.admin.sites import AdminSite
from datetime import datetime
from datetime import timedelta

from .forms import *
from .models import *
from .admin import *

# This is a really slow test that covers all combinations of recurrence, turn it false to skip it for a faster test
TEST_CREATE_EDIT_CONFLIC_RECURRENT = True

class MockRequest:
    GET = list()
    def build_absolute_uri(self, pru):
        return '/pru/'
request = MockRequest()
class AdminViewPermissionsTests(TestCase):

    def create_preset(self):
        # Create users with different prioritys
        # Also gives them all permissions and staff so they can see admin page
        permissions = Permission.objects.all()
        common = User.objects.create_user('common', password='a')
        common.is_staff=True
        common.user_permissions.set(permissions)
        common.save()
        item_responsable = User.objects.create_user('item_responsable', password='a')
        item_responsable.is_staff=True
        item_responsable.user_permissions.set(permissions)
        item_responsable.save()
        sub_unit_responsable = User.objects.create_user('sub_unit_responsable', password='a')
        sub_unit_responsable.is_staff=True
        sub_unit_responsable.user_permissions.set(permissions)
        sub_unit_responsable.save()
        unit_responsable = User.objects.create_user('unit_responsable', password='a')
        unit_responsable.is_staff=True
        unit_responsable.user_permissions.set(permissions)
        unit_responsable.save()
        superuser = User.objects.create_user('superuser', password='a')
        superuser.is_superuser=True
        superuser.is_staff=True
        superuser.save()

        # Create units to their respective responsable
        parentUnit = Unidade.objects.create(sigla='pu', nome='parent unit', descricao='test')
        parentUnit.save()
        parentUnit.responsavel.add(unit_responsable)
        childUnit = Unidade.objects.create(sigla='cu', nome='child unit', unidadePai=parentUnit, descricao='test')
        parentUnit.save()
        childUnit.responsavel.add(sub_unit_responsable)

        # Create a room and a equipment and a service for each user (except common)
        room0 = EspacoFisico.objects.create(nome='room0', descricao='test', unidade=childUnit, capacidade=0)
        room0.save()
        room0.responsavel.add(item_responsable)
        equipment0 = Equipamento.objects.create(nome='equipment0', descricao='test', unidade=childUnit, patrimonio=0)
        equipment0.save()
        equipment0.responsavel.add(item_responsable)
        service0 = Servico.objects.create(nome='service0', descricao='test', unidade=childUnit)
        service0.save()
        service0.responsavel.add(item_responsable)
        room1 = EspacoFisico.objects.create(nome='room1', descricao='test', unidade=childUnit, capacidade=0)
        room1.save()
        room1.responsavel.add(sub_unit_responsable)
        equipment1 = Equipamento.objects.create(nome='equipment1', descricao='test', unidade=childUnit, patrimonio=0)
        equipment1.save()
        equipment1.responsavel.add(sub_unit_responsable)
        service1 = Servico.objects.create(nome='service1', descricao='test', unidade=childUnit)
        service1.save()
        service1.responsavel.add(sub_unit_responsable)
        room2 = EspacoFisico.objects.create(nome='room2', descricao='test', unidade=parentUnit, capacidade=0)
        room2.save()
        room2.responsavel.add(unit_responsable)
        equipment2 = Equipamento.objects.create(nome='equipment2', descricao='test', unidade=parentUnit, patrimonio=0)
        equipment2.save()
        equipment2.responsavel.add(unit_responsable)
        service2 = Servico.objects.create(nome='service2', descricao='test', unidade=parentUnit)
        service2.save()
        service2.responsavel.add(unit_responsable)

        # Create a activitie (required for reserve)
        activitie = Atividade.objects.create(nome='activitie', descricao='default')

        # Create a reserve for both room and equipment for each user
        reserve_room0 = ReservaEspacoFisico.objects.create(data='1000-10-10', horaInicio='00:00', horaFim='00:00', atividade=activitie, usuario=common, ramal=0, finalidade='t', locavel=room0)
        reserve_room0.save()
        reserve_equipment0 = ReservaEquipamento.objects.create(data='1000-10-10', horaInicio='00:00', horaFim='00:00', atividade=activitie, usuario=common, ramal=0, finalidade='t', locavel=equipment0)
        reserve_equipment0.save()
        reserve_service0 = ReservaServico.objects.create(data='1000-10-10', horaInicio='00:00', horaFim='00:00', atividade=activitie, usuario=common, ramal=0, finalidade='t', locavel=service0)
        reserve_service0.save()
        reserve_room1 = ReservaEspacoFisico.objects.create(data='1000-10-10', horaInicio='00:00', horaFim='00:00', atividade=activitie, usuario=item_responsable, ramal=0, finalidade='t', locavel=room1)
        reserve_room1.save()
        reserve_equipment1 = ReservaEquipamento.objects.create(data='1000-10-10', horaInicio='00:00', horaFim='00:00', atividade=activitie, usuario=item_responsable, ramal=0, finalidade='t', locavel=equipment1)
        reserve_equipment1.save()
        reserve_service1 = ReservaServico.objects.create(data='1000-10-10', horaInicio='00:00', horaFim='00:00', atividade=activitie, usuario=item_responsable, ramal=0, finalidade='t', locavel=service1)
        reserve_service1.save()
        reserve_room2 = ReservaEspacoFisico.objects.create(data='1000-10-10', horaInicio='00:00', horaFim='00:00', atividade=activitie, usuario=sub_unit_responsable, ramal=0, finalidade='t', locavel=room2)
        reserve_room2.save()
        reserve_equipment2 = ReservaEquipamento.objects.create(data='1000-10-10', horaInicio='00:00', horaFim='00:00', atividade=activitie, usuario=sub_unit_responsable, ramal=0, finalidade='t', locavel=equipment2)
        reserve_equipment2.save()
        reserve_service2 = ReservaServico.objects.create(data='1000-10-10', horaInicio='00:00', horaFim='00:00', atividade=activitie, usuario=sub_unit_responsable, ramal=0, finalidade='t', locavel=service2)
        reserve_service2.save()

        return {'rooms': [room0, room1, room2],
                'equipments': [equipment0, equipment1, equipment2],
                'services': [service0, service1, service2],
                'room_reserves': [reserve_room0, reserve_room1, reserve_room2],
                'equipment_reserves': [reserve_equipment0, reserve_equipment1, reserve_equipment2],
                'service_reserves': [reserve_service0, reserve_service1, reserve_service2]}

    def check_items(self, user, items, room=True, equipment=True, service=True):
        request.user = user
        if room:
            ma = EspacoFisicoAdmin(EspacoFisico, AdminSite())
            rooms = list(ma.get_queryset(request))
            self.assertCountEqual(rooms, items['rooms'])
        if equipment:
            ma = EquipamentoAdmin(Equipamento, AdminSite())
            equipments = list(ma.get_queryset(request))
            self.assertCountEqual(equipments, items['equipments'])
        if service:
            ma = ServicoAdmin(Servico, AdminSite())
            services = list(ma.get_queryset(request))
            self.assertCountEqual(services, items['services'])
        ma  = ReservaEspacoFisicoAdmin(ReservaEspacoFisico, AdminSite())
        room_reserves = list(ma.get_queryset(request))
        self.assertCountEqual(room_reserves, items['room_reserves'])
        ma = ReservaEquipamentoAdmin(ReservaEquipamento, AdminSite())
        equipment_reserves = list(ma.get_queryset(request))
        self.assertCountEqual(equipment_reserves, items['equipment_reserves'])
        ma = ReservaServicoAdmin(ReservaServico, AdminSite())
        service_reserves = list(ma.get_queryset(request))
        self.assertCountEqual(service_reserves, items['service_reserves'])

    def test_admin_view_filter(self):
        print('TESTING ADMIN VIEW FILTER')
        items = self.create_preset()

        # First superuser, he must see everything in items
        user = User.objects.get(username='superuser')
        self.check_items(user, items)
        print('-SUPERUSER CASE PASS')

        # Unit_responsable also must see every item, even though he's not responsable for reserves
        user = User.objects.get(username='unit_responsable')
        self.check_items(user, items)
        print('-UNIT RESPONSABLE CASE PASS')

        # Sub_unit_responsable must be able to see everything but room and equipment and service 2
        user = User.objects.get(username='sub_unit_responsable')
        request.user = user
        ma = EspacoFisicoAdmin(EspacoFisico, AdminSite())
        rooms = list(ma.get_queryset(request))
        self.assertEqual(2, len(rooms))
        temp = list(items['rooms'])
        temp.pop()
        self.assertCountEqual(temp, rooms)

        ma = EquipamentoAdmin(Equipamento, AdminSite())
        equipments = list(ma.get_queryset(request))
        self.assertEqual(2, len(equipments))
        temp = list(items['equipments'])
        temp.pop()
        self.assertCountEqual(temp, equipments)

        ma = ServicoAdmin(Servico, AdminSite())
        services = list(ma.get_queryset(request))
        self.assertEqual(2, len(services))
        temp = list(items['services'])
        temp.pop()
        self.assertCountEqual(temp, services)

        self.check_items(user, items, room=False, equipment=False, service=False)
        print('-SUB UNIT RESPONSABLE CASE PASS')

        # Item responsable can only see rooms and equipments and services 0 and reserves 0 and 1
        user = User.objects.get(username='item_responsable')
        request.user = user

        ma = EspacoFisicoAdmin(EspacoFisico, AdminSite())
        rooms = list(ma.get_queryset(request))
        self.assertEqual(1, len(rooms))
        temp = list(items['rooms'])
        temp.pop()
        temp.pop()
        self.assertCountEqual(temp, rooms)

        ma = EquipamentoAdmin(Equipamento, AdminSite())
        equipments = list(ma.get_queryset(request))
        self.assertEqual(1, len(equipments))
        temp = list(items['equipments'])
        temp.pop()
        temp.pop()
        self.assertCountEqual(temp, equipments)

        ma = ServicoAdmin(Servico, AdminSite())
        services = list(ma.get_queryset(request))
        self.assertEqual(1, len(services))
        temp = list(items['services'])
        temp.pop()
        temp.pop()
        self.assertCountEqual(temp, services)  

        ma = ReservaEspacoFisicoAdmin(ReservaEspacoFisico, AdminSite())
        room_reserves = list(ma.get_queryset(request))
        self.assertEqual(2, len(room_reserves))
        temp = list(items['room_reserves'])
        temp.pop()
        self.assertCountEqual(temp, room_reserves)

        ma = ReservaEquipamentoAdmin(ReservaEquipamento, AdminSite())
        equipment_reserves = list(ma.get_queryset(request))
        self.assertEqual(2, len(equipment_reserves))
        temp = list(items['equipment_reserves'])
        temp.pop()
        self.assertCountEqual(temp, equipment_reserves)

        ma = ReservaServicoAdmin(ReservaServico, AdminSite())
        service_reserves = list(ma.get_queryset(request))
        self.assertEqual(2, len(service_reserves))
        temp = list(items['service_reserves'])
        temp.pop()
        self.assertCountEqual(temp, service_reserves)
        print('-ITEM RESPONSABLE CASE PASS')

        # Common user can only see reserves 0
        user = User.objects.get(username='common')
        request.user = user

        ma = EspacoFisicoAdmin(EspacoFisico,AdminSite())
        rooms = list(ma.get_queryset(request))
        self.assertEqual(0, len(rooms))

        ma = EquipamentoAdmin(Equipamento, AdminSite())
        equipments = list(ma.get_queryset(request))
        self.assertEqual(0, len(equipments))

        ma = ServicoAdmin(Servico, AdminSite())
        services = list(ma.get_queryset(request))
        self.assertEqual(0, len(services))

        ma = ReservaEquipamentoAdmin(ReservaEquipamento, AdminSite())
        equipment_reserves = list(ma.get_queryset(request))
        self.assertEqual(1, len(equipment_reserves))
        temp = list(items['equipment_reserves'])
        temp.pop()
        temp.pop()
        self.assertCountEqual(temp, equipment_reserves)

        ma = ReservaEspacoFisicoAdmin(ReservaEspacoFisico, AdminSite())
        room_reserves = list(ma.get_queryset(request))
        self.assertEqual(1, len(room_reserves))
        temp = list(items['room_reserves'])
        temp.pop()
        temp.pop()
        self.assertCountEqual(temp, room_reserves)

        ma = ReservaServicoAdmin(ReservaServico, AdminSite())
        service_reserves = list(ma.get_queryset(request))
        self.assertEqual(1, len(service_reserves))
        temp = list(items['service_reserves'])
        temp.pop()
        temp.pop()
        self.assertCountEqual(temp, service_reserves)
        print('-COMMON USER CASE PASS')

    def test_reserve_search(self):
        print('-TESTING SEARCHING IN RESERVE ADMIN')
        things = self.create_preset()
        things['room_reserves'][0].estado = 'A'
        things['room_reserves'][0].save()
        things['room_reserves'][2].estado = 'D'
        things['room_reserves'][2].save()
        queryset = ReservaEspacoFisico.objects.all()
        ma = ReservaEspacoFisicoAdmin(ReservaEspacoFisico, AdminSite())
        result, pru = ma.get_search_results(request, queryset, 'aprovado')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0], things['room_reserves'][0])
        result, pru = ma.get_search_results(request, queryset, 'esperando')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0], things['room_reserves'][1])
        result, pru = ma.get_search_results(request, queryset, 'desaprovado')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0], things['room_reserves'][2])

        things['equipment_reserves'][0].estado = 'A'
        things['equipment_reserves'][0].save()
        things['equipment_reserves'][2].estado = 'D'
        things['equipment_reserves'][2].save()
        queryset = ReservaEquipamento.objects.all()
        ma = ReservaEquipamentoAdmin(ReservaEquipamento, AdminSite())
        result, pru = ma.get_search_results(request, queryset, 'aprovado')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0], things['equipment_reserves'][0])
        result, pru = ma.get_search_results(request, queryset, 'esperando')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0], things['equipment_reserves'][1])
        result, pru = ma.get_search_results(request, queryset, 'desaprovado')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0], things['equipment_reserves'][2])

        things['service_reserves'][0].estado = 'A'
        things['service_reserves'][0].save()
        things['service_reserves'][2].estado = 'D'
        things['service_reserves'][2].save()
        queryset = ReservaServico.objects.all()
        ma = ReservaServicoAdmin(ReservaServico, AdminSite())
        result, pru = ma.get_search_results(request, queryset, 'aprovado')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0], things['service_reserves'][0])
        result, pru = ma.get_search_results(request, queryset, 'esperando')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0], things['service_reserves'][1])
        result, pru = ma.get_search_results(request, queryset, 'desaprovado')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0], things['service_reserves'][2])

        print('-SEARCHING IN RESERVE ADMIN TEST PASSED')

    def check_delete_permission(self, admin_type, reserve_type, users, superuser):
        request.user = superuser
        ma = admin_type(reserve_type, AdminSite())
        self.assertTrue(ma.has_delete_permission(request))
        if 'delete_selected' not in ma.get_actions(request):
            self.fail("Superuser doesn't have delete permission!")

        for user in users:
            request.user = user
            ma = admin_type(reserve_type, AdminSite())
            self.assertFalse(ma.has_delete_permission(request))
            if 'delete_selected' in ma.get_actions(request):
                self.fail("Non superuser have delete permission!")

    def test_delete_permission(self):
        print '-TESTING DELETE PERMISSION'
        self.create_preset()
        superuser = User.objects.get(username='superuser')
        users = list(User.objects.all().exclude(username='superuser'))
        self.check_delete_permission(ReservaEspacoFisicoAdmin, ReservaEspacoFisico, users, superuser)
        self.check_delete_permission(ReservaEquipamentoAdmin, ReservaEquipamento, users, superuser)
        self.check_delete_permission(ReservaServicoAdmin, ReservaServico, users, superuser)
        print '-DELETE PERMISSION TEST PASSED'

class UserFilterTests(TestCase):
    def createPreset(self):
        # Create one superuser to be responsable for everything
        superuser = User.objects.create(username='superuser', password='a')
        # Create the units in a binary tree fashion
        root = Unidade.objects.create(sigla='rt', nome='root', descricao='test')
        root.save()
        root.responsavel.add(superuser)
        child_left = Unidade.objects.create(sigla='cl', nome='child_left', unidadePai=root, descricao='test')
        child_left.save()
        child_left.responsavel.add(superuser)
        child_left.responsavel.add(superuser)
        child_left_left = Unidade.objects.create(sigla='cll', nome='child_left_left', unidadePai=child_left, descricao='q')
        child_left_left.save()
        child_left_left.responsavel.add(superuser)
        child_left_right = Unidade.objects.create(sigla='clr', nome='child_left_right', unidadePai=child_left, descricao='')
        child_left_right.save()
        child_left_right.responsavel.add(superuser)
        child_right = Unidade.objects.create(sigla='cr', nome='child_right', unidadePai=root, descricao='q')
        child_right.save()
        child_left_right.responsavel.add(superuser)
        child_right_left = Unidade.objects.create(sigla='crl', nome='child_right_left', unidadePai=child_right, descricao='q')
        child_right_left.save()
        child_right_left.responsavel.add(superuser)
        child_right_right = Unidade.objects.create(sigla='crr', nome='child_right_right', unidadePai=child_right, descricao='q')
        child_right_right.save()
        child_right_right.responsavel.add(superuser)
        child_right_right_left = Unidade.objects.create(sigla='crrl', nome='child_right_right_left', unidadePai=child_right_right, descricao='q')
        child_right_right_left.save()
        child_right_right_left.responsavel.add(superuser)

        # Create equipments and places with different characteristics in "leaf" units
        invisible_place = EspacoFisico.objects.create(nome='inivisible_place', descricao='q', unidade=child_left_left, invisivel=True, localizacao='q', capacidade=1)
        invisible_place.save()
        invisible_equipment = Equipamento.objects.create(nome='invisible_equipment', descricao='q', unidade=child_left_left, invisivel=True, localizacao='q', patrimonio=3)
        invisible_equipment.save()
        invisible_service = Servico.objects.create(nome='invisible_service', descricao='q', unidade=child_left_left, invisivel=True, localizacao='q')
        invisible_service.save()
        group_place = EspacoFisico.objects.create(nome='group_place', descricao='q', unidade=child_left_left, localizacao='q', capacidade=2)
        group_place.save()
        group_equipment = Equipamento.objects.create(nome='group_equipment', descricao='q', unidade=child_left_left, localizacao='q', patrimonio=2)
        group_equipment.save()
        group_service = Servico.objects.create(nome='group_service', descricao='q', unidade=child_left_left, localizacao='q')
        group_service.save()
        place0 = EspacoFisico.objects.create(nome='place0', descricao='q', unidade=child_left_right, localizacao='q', capacidade=2)
        place0.save()
        equipment0 = Equipamento.objects.create(nome='equipment0', descricao='q', unidade=child_left_right, localizacao='q', patrimonio=2)
        equipment0.save()
        service0 = Servico.objects.create(nome='service0', descricao='q', unidade=child_left_right, localizacao='q')
        service0.save()
        place1 = EspacoFisico.objects.create(nome='place1', descricao='q', unidade=child_right_left, localizacao='q', capacidade=2)
        place1.save()
        equipment1 = Equipamento.objects.create(nome='equipment1', descricao='q', unidade=child_right_left, localizacao='q', patrimonio=1)
        equipment1.save()
        service1 = Servico.objects.create(nome='service1', descricao='q', unidade=child_right_left, localizacao='q')
        service1.save()
        place2 = EspacoFisico.objects.create(nome='place2', descricao='q', unidade=child_right_right_left, localizacao='q', capacidade=2)
        place2.save()
        equipment2 = Equipamento.objects.create(nome='equipment2', descricao='q', unidade=child_right_right_left, localizacao='q', patrimonio=2)
        equipment2.save()
        service2 = Servico.objects.create(nome='service2', descricao='q', unidade=child_right_right_left, localizacao='q')
        service2.save()
        blocked_place = EspacoFisico.objects.create(nome='blocked_place', descricao='q', unidade=child_right_right, bloqueado=True, localizacao='q', capacidade=2)
        blocked_place.save()
        blocked_equipment = Equipamento.objects.create(nome='blocked_equipment', descricao='q', unidade=child_right_right, bloqueado=True, localizacao=2, patrimonio=2)
        blocked_equipment.save()
        blocked_service = Servico.objects.create(nome='blocked_service', descricao='q', unidade=child_right_right, bloqueado=True, localizacao=2)
        blocked_service.save()

        # Create common users
        root_user = User.objects.create(username='root_user', password='a')
        root_user.save()
        child_left_user = User.objects.create(username='child_left_user', password='a')
        child_left_user.save()
        root_group_user = User.objects.create(username='root_group_user', password='a')
        root_group_user.save()

        # Creat unit groups and add people, units and place/equiptment to it
        group_x = Group.objects.create(name='group_x')
        group_x.unidade_set.add(root)
        group_x.user_set.add(root_user)
        root.grupos.add(group_x)
        group_x.user_set.add(root_group_user)

        group_y = Group.objects.create(name='group_y')
        group_y.unidade_set.add(child_left)
        group_y.user_set.add(child_left_user)
        child_left.grupos.add(group_y)

        child_right_right.grupos.add(group_x)
        child_right_right.grupos.add(group_y)
        group_x.unidade_set.add(child_right_right)
        group_y.unidade_set.add(child_right_right)

        permission = Group.objects.create(name='permission')
        permission.espacofisico_set.add(group_place)
        group_place.grupos.add(permission)

        permission.equipamento_set.add(group_equipment)
        group_equipment.grupos.add(permission)

        permission.servico_set.add(group_service)
        group_service.grupos.add(permission)

        permission.user_set.add(root_group_user)

        return {
            'places': [invisible_place, group_place, place0, place1, place2, blocked_place],
            'equipments': [invisible_equipment, group_equipment, equipment0, equipment1, equipment2, blocked_equipment],
            'services': [invisible_service, group_service, service0, service1, service2, blocked_service]
        }

    def makeChecks(self, items, user, pop_items):
        # pop items user shouldn't see
        places = list(items['places'])
        equipments = list(items['equipments'])
        services = list(items['services'])
        for item in pop_items:
            places.pop(item)
            equipments.pop(item)
            services.pop(item)

        # Create user, get options and compare
        user = User.objects.get(username=user)
        request.user = user
        ma = EspacoFisicoAdmin(EspacoFisico, AdminSite())
        bd_places = list(ma.get_queryset(request))
        self.assertCountEqual(bd_places, places)

        ma = EquipamentoAdmin(Equipamento, AdminSite())
        bd_equipments = list(ma.get_queryset(request))
        self.assertCountEqual(bd_equipments, equipments)

        ma = ServicoAdmin(Servico, AdminSite())
        bd_services = list(ma.get_queryset(request))
        self.assertCountEqual(bd_services, services)

    def test_user_groups_filter(self):
        items = self.createPreset()

        print('-TESTING GROUP FILTERS')

        # Superuser must see everything since he's responsable
        self.makeChecks(items, 'superuser', [])
        # Root user (whithout group) must see item 2, 3 and blocked
        self.makeChecks(items, 'root_user', [0, 0, 0])
        # Child_left user must see item 1, 3 and blocked
        self.makeChecks(items, 'child_left_user', [0, 0, 1])
        # root_group_user must see item 2, 3, blocked and group
        self.makeChecks(items, 'root_group_user', [0, 1])

        print('-GROUP FILTERS PASS')

class FormTests(TestCase):

    def create_preset(self):

        # create models
        activitie = Atividade.objects.create(nome='activitie', descricao='default')
        activitie.save()
        responsable = User.objects.create_user('responsable', password='a')
        responsable.save()
        unit = Unidade.objects.create(sigla='pru', nome='unit', descricao='test')
        unit.responsavel.add(responsable)
        unit.save()
        physical_space = EspacoFisico.objects.create(nome='physical_space', descricao='q', unidade=unit, bloqueado=False, localizacao='q', capacidade=2)
        physical_space.responsavel.add(responsable)
        physical_space.atividadesPermitidas.add(activitie)
        physical_space.save()
        equipment = Equipamento.objects.create(nome='equipment', descricao='q', unidade=unit, localizacao='q', patrimonio=2)
        equipment.responsavel.add(responsable)
        equipment.atividadesPermitidas.add(activitie)
        equipment.save()
        service = Servico.objects.create(nome='service', descricao='q', unidade=unit, localizacao='q')
        service.responsavel.add(responsable)
        service.atividadesPermitidas.add(activitie)
        service.save()
        no_permission_user = User.objects.create_user('no_permission_user', password='a')
        no_permission_user.save()
        permission_user = User.objects.create_user('permission_user', password='a')
        permission_user.save()

        # give permissions so users can create stuff
        permissions = Permission.objects.all()
        responsable.user_permissions.set(permissions)
        responsable.save()
        no_permission_user.user_permissions.set(permissions)
        no_permission_user.save()
        permission_user.user_permissions.set(permissions)
        permission_user.save()

        # create a group to the unit
        group = Group.objects.create(name='group')
        unit.grupos.add(group)
        group.user_set.add(permission_user)
        unit.save()
        group.save()

    def create_form(self, reserve_type, form_type, status, date, recurrent, ending_date, starting_time, ending_time, reservable, user, instance=None
        , starting_reservable=False, mon=False, tue=False, wed=False, thu=False, fri=False, sat=False, sun=False):
        date = datetime.strptime(date, '%d/%m/%Y').date()
        if ending_date:
            ending_date = datetime.strptime(ending_date, '%d/%m/%Y').date()
        starting_time = datetime.strptime(starting_time, '%H:%M').time()
        ending_time = datetime.strptime(ending_time, '%H:%M').time()
        activitie = Atividade.objects.get(nome='activitie')
        ramal = 6
        reason = 'test'
        request.user = user
        request.session = dict()
        if starting_reservable:
            request.session['id_reservable'] = reservable.id
        def a(a):
            return ''
        request.build_absolute_uri = a
        form = form_type(data={
            'estado': status,
            'data': date,
            'recorrente': recurrent,
            'seg': mon,
            'ter': tue,
            'qua': wed,
            'qui': thu,
            'sex': fri,
            'sab': sat,
            'dom': sun,
            'dataFim': ending_date,
            'horaInicio': starting_time,
            'horaFim': ending_time,
            'locavel': reservable.pk,
            'atividade': activitie.pk,
            'usuario': user.pk,
            'ramal': ramal,
            'finalidade': reason,
        }, initial={'recorrente': recurrent}, request=request, instance=instance)
        return form

    def test_reserve_form(self):
        print('-TESTING RESERVE FORM')
        self.create_preset()
        responsable = User.objects.get(username='responsable')
        permission_user = User.objects.get(username='permission_user')
        no_permission_user = User.objects.get(username='no_permission_user')
        physical_space = EspacoFisico.objects.get(nome='physical_space')
        equipment = Equipamento.objects.get(nome='equipment')
        service = Servico.objects.get(nome='service')
        unit = Unidade.objects.get(nome='unit')

        self.auto_approve_test(responsable, permission_user, no_permission_user, physical_space, equipment, service)
        self.recurrent_reserve_test(responsable, permission_user, no_permission_user, physical_space, equipment, service)
        self.model_clean_tests(no_permission_user, responsable, physical_space, equipment, service, unit)
        self.unit_form_test(unit, no_permission_user)
        self.group_only_test(responsable, permission_user, no_permission_user, physical_space, equipment, service)
        self.status_options_test(responsable, permission_user, no_permission_user, physical_space, equipment, service)

        print('-RESERVE FORM TEST PASSED')


    def auto_approve_test(self, responsable, permission_user, no_permission_user, physical_space, equipment, service):
        print('--TESTING AUTO APPROVE')
        # Test responsable making reserve
        form = self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', physical_space, responsable)
        form.save()
        instance = ReservaEspacoFisico.objects.all()[0]
        self.assertEqual(instance.estado, 'A')
        instance.delete()
        form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', equipment, responsable)
        form.save()
        instance = ReservaEquipamento.objects.all()[0]
        self.assertEqual(instance.estado, 'A')
        instance.delete()
        form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', service, responsable)
        form.save()
        instance = ReservaServico.objects.all()[0]
        self.assertEqual(instance.estado, 'A')
        instance.delete()

        # Test user in group making reserve
        form = self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', physical_space, permission_user)
        form.save()
        instance = ReservaEspacoFisico.objects.all()[0]
        self.assertEqual(instance.estado, 'A')
        instance.delete()
        form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', equipment, permission_user)
        form.save()
        instance = ReservaEquipamento.objects.all()[0]
        self.assertEqual(instance.estado, 'A')
        instance.delete()
        form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', service, permission_user)
        form.save()
        instance = ReservaServico.objects.all()[0]
        self.assertEqual(instance.estado, 'A')
        instance.delete()

        # Test user not in group making reserve
        form = self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', physical_space, no_permission_user)
        form.save()
        instance = ReservaEspacoFisico.objects.all()[0]
        self.assertEqual(instance.estado, 'E')
        instance.delete()
        form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', equipment, no_permission_user)
        form.save()
        instance = ReservaEquipamento.objects.all()[0]
        self.assertEqual(instance.estado, 'E')
        instance.delete()
        form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', service, no_permission_user)
        form.save()
        instance = ReservaServico.objects.all()[0]
        self.assertEqual(instance.estado, 'E')
        instance.delete()

        # Test if reservable needs responsable approval
        physical_space.permissaoNecessaria = True
        physical_space.save()
        form = self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', physical_space, permission_user)
        form.save()
        instance = ReservaEspacoFisico.objects.all()[0]
        self.assertEqual(instance.estado, 'E')
        instance.delete()
        physical_space.permissaoNecessaria = False
        physical_space.save()
        equipment.permissaoNecessaria = True
        equipment.save()
        form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', equipment, permission_user)
        form.save()
        instance = ReservaEquipamento.objects.all()[0]
        self.assertEqual(instance.estado, 'E')
        instance.delete()
        equipment.permissaoNecessaria = False
        equipment.save()
        service.permissaoNecessaria = True
        service.save()
        form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', service, permission_user)
        form.save()
        instance = ReservaServico.objects.all()[0]
        self.assertEqual(instance.estado, 'E')
        instance.delete()
        service.permissaoNecessaria = False
        service.save()

        print('--AUTO APPROVE TEST PASSED')

    def create_edit_conflict_recurrent_test(self, responsable, permission_user, no_permission_user, physical_space, equipment, service):
        possibilitie = 1
        possibilitie_b = "{0:07b}".format(possibilitie)
        while possibilitie_b != '1111111':
            self.create_recurrent_reserve_test(possibilitie_b, responsable, permission_user, no_permission_user, physical_space, equipment, service)
            possibilitie = possibilitie + 1
            possibilitie_b = "{0:07b}".format(possibilitie)

    def recurrent_week_days_boolean(self, possibilitie_b):
        week_days = list()
        if possibilitie_b[-1] == '1':
            week_days.append(True)
        else:
            week_days.append(False)
        if possibilitie_b[-2] == '1':
            week_days.append(True)
        else:
            week_days.append(False)
        if possibilitie_b[-3] == '1':
            week_days.append(True)
        else:
            week_days.append(False)
        if possibilitie_b[-4] == '1':
            week_days.append(True)
        else:
            week_days.append(False)
        if possibilitie_b[-5] == '1':
            week_days.append(True)
        else:
            week_days.append(False)
        if possibilitie_b[-6] == '1':
            week_days.append(True)
        else:
            week_days.append(False)
        if possibilitie_b[-7] == '1':
            week_days.append(True)
        else:
            week_days.append(False)
        return week_days

    def recurrent_week_days_number(self, possibilitie_b):
        week_days = list()
        if possibilitie_b[-1] == '1':
            week_days.append(0)

        if possibilitie_b[-2] == '1':
            week_days.append(1)

        if possibilitie_b[-3] == '1':
            week_days.append(2)

        if possibilitie_b[-4] == '1':
            week_days.append(3)

        if possibilitie_b[-5] == '1':
            week_days.append(4)

        if possibilitie_b[-6] == '1':
            week_days.append(5)

        if possibilitie_b[-7] == '1':
            week_days.append(6)
        return week_days

    def create_recurrent_reserve_test(self, possibilitie_b, responsable, permission_user, no_permission_user, physical_space, equipment, service):
        N_WEEKS = 4  # test are done from 01/06/9999 to 22/06/9999, 4 weeks
        STARTING_DAY = '31/05/9999'
        ENDING_DAY = '27/06/9999'
        expected_reserves = 0
        week_days_boolean = self.recurrent_week_days_boolean(possibilitie_b)
        week_days_number = self.recurrent_week_days_number(possibilitie_b)
        for recurrent_day in week_days_boolean:
            if recurrent_day:
                expected_reserves = expected_reserves + N_WEEKS

        # Create reserve
        form = self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'E', STARTING_DAY, True, ENDING_DAY, '00:01', '00:02', physical_space, no_permission_user,
            mon=week_days_boolean[0], tue=week_days_boolean[1], wed=week_days_boolean[2], thu=week_days_boolean[3], fri=week_days_boolean[4], sat=week_days_boolean[5], sun=week_days_boolean[6])
        form.save()
        form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'E', STARTING_DAY, True, ENDING_DAY, '00:01', '00:02', equipment, no_permission_user,
            mon=week_days_boolean[0], tue=week_days_boolean[1], wed=week_days_boolean[2], thu=week_days_boolean[3], fri=week_days_boolean[4], sat=week_days_boolean[5], sun=week_days_boolean[6])
        form.save()
        form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'E', STARTING_DAY, True, ENDING_DAY, '00:01', '00:02', service, no_permission_user,
            mon=week_days_boolean[0], tue=week_days_boolean[1], wed=week_days_boolean[2], thu=week_days_boolean[3], fri=week_days_boolean[4], sat=week_days_boolean[5], sun=week_days_boolean[6])
        form.save()

        # Test reserve info
        all_querys = (ReservaEspacoFisico.objects.all(), ReservaEquipamento.objects.all(), ReservaServico.objects.all())
        for query in all_querys:
            self.assertEqual(len(query), expected_reserves)
            current_date = datetime.strptime(STARTING_DAY, '%d/%m/%Y').date()
            expected_dates = list()
            while current_date <= datetime.strptime(ENDING_DAY, '%d/%m/%Y').date():
                if current_date.weekday() in week_days_number:
                    expected_dates.append(current_date)
                current_date = current_date + timedelta(days=1)
            for reserve in query:
                self.assertEqual(reserve.data, expected_dates.pop(0))

        # Testing edit recurrent reserve
        instance = ReservaEspacoFisico.objects.all()[0]
        form = self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'A', STARTING_DAY, True, ENDING_DAY, '00:01', '00:02', physical_space, responsable, instance,
            mon=week_days_boolean[0], tue=week_days_boolean[1], wed=week_days_boolean[2], thu=week_days_boolean[3], fri=week_days_boolean[4], sat=week_days_boolean[5], sun=week_days_boolean[6])
        form.is_valid()
        form.save()
        query = ReservaEspacoFisico.objects.all()
        for reserve in query:
            self.assertEqual(reserve.estado, 'A')
        instance = ReservaEquipamento.objects.all()[0]
        form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'A', STARTING_DAY, True, ENDING_DAY, '00:01', '00:02', equipment, responsable, instance,
            mon=week_days_boolean[0], tue=week_days_boolean[1], wed=week_days_boolean[2], thu=week_days_boolean[3], fri=week_days_boolean[4], sat=week_days_boolean[5], sun=week_days_boolean[6])
        form.is_valid()
        form.save()
        query = ReservaEquipamento.objects.all()
        for reserve in query:
            self.assertEqual(reserve.estado, 'A')
        instance = ReservaServico.objects.all()[0]
        form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'A', STARTING_DAY, True, ENDING_DAY, '00:01', '00:02', service, responsable, instance,
            mon=week_days_boolean[0], tue=week_days_boolean[1], wed=week_days_boolean[2], thu=week_days_boolean[3], fri=week_days_boolean[4], sat=week_days_boolean[5], sun=week_days_boolean[6])
        form.is_valid()
        form.save()
        query = ReservaServico.objects.all()
        for reserve in query:
            self.assertEqual(reserve.estado, 'A')

        # Test datetime conflict
        form = self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'A', STARTING_DAY, True, ENDING_DAY, '00:01', '00:02', physical_space, no_permission_user,
            mon=week_days_boolean[0], tue=week_days_boolean[1], wed=week_days_boolean[2], thu=week_days_boolean[3], fri=week_days_boolean[4], sat=week_days_boolean[5], sun=week_days_boolean[6])
        self.assertIs(form.is_valid(), False)
        form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'A', STARTING_DAY, True, ENDING_DAY, '00:01', '00:02', equipment, no_permission_user,
            mon=week_days_boolean[0], tue=week_days_boolean[1], wed=week_days_boolean[2], thu=week_days_boolean[3], fri=week_days_boolean[4], sat=week_days_boolean[5], sun=week_days_boolean[6])
        self.assertIs(form.is_valid(), False)
        form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'A', STARTING_DAY, True, ENDING_DAY, '00:01', '00:02', service, no_permission_user,
            mon=week_days_boolean[0], tue=week_days_boolean[1], wed=week_days_boolean[2], thu=week_days_boolean[3], fri=week_days_boolean[4], sat=week_days_boolean[5], sun=week_days_boolean[6])
        self.assertIs(form.is_valid(), False)

        ReservaEspacoFisico.objects.all().delete()
        ReservaEquipamento.objects.all().delete()
        ReservaServico.objects.all().delete()

    def recurrent_reserve_test(self, responsable, permission_user, no_permission_user, physical_space, equipment, service):
        if TEST_CREATE_EDIT_CONFLIC_RECURRENT:
            print('--TESTING CREATE RECURRENT RESERVE')
            self.create_edit_conflict_recurrent_test(responsable, permission_user, no_permission_user, physical_space, equipment, service)
            print('--CREATE RECURRENT RESERVE TEST PASSED')

        #  Ending date must be necessary only if recurrent
        print('--TESTING ENDING DATE NECESSARY WHEN RECURRENT')
        form = self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'A', '24/09/9999', True, None, '00:01', '00:02', physical_space, no_permission_user, mon=True)
        self.assertIs(form.is_valid(), False)
        form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'A', '24/09/9999', True, None, '00:01', '00:02', equipment, no_permission_user, mon=True)
        self.assertIs(form.is_valid(), False)
        form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'A', '24/09/9999', True, None, '00:01', '00:02', service, no_permission_user, mon=True)
        self.assertIs(form.is_valid(), False)
        form = self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'A', '24/09/9999', False, None, '00:01', '00:02', physical_space, no_permission_user, mon=True)
        self.assertIs(form.is_valid(), True)
        form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'A', '24/09/9999', False, None, '00:01', '00:02', equipment, no_permission_user, mon=True)
        self.assertIs(form.is_valid(), True)
        form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'A', '24/09/9999', False, None, '00:01', '00:02', service, no_permission_user, mon=True)
        self.assertIs(form.is_valid(), True)
        print('--ENDING DATE NECESSARY WHEN RECURRENT TEST PASSED')

        #  If starting date is bigger than ending, form is invalid
        print('--TESTING ENDING AFTER STARTING DATE')
        form = self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'A', '24/06/9999', True, '23/06/9999', '00:01', '00:02', physical_space, no_permission_user, mon=True)
        self.assertIs(form.is_valid(), False)
        form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'A', '24/06/9999', True, '23/06/9999', '00:01', '00:02', equipment, no_permission_user, mon=True)
        self.assertIs(form.is_valid(), False)
        form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'A', '24/06/9999', True, '23/06/9999', '00:01', '00:02', service, no_permission_user, mon=True)
        self.assertIs(form.is_valid(), False)
        print('--ENDING AFTER STARTING TEST PASSED')

        # ending date can't pass max advance
        print('--TESTING MAX ADVANCE RESERVE IN RECURRENT')
        physical_space.antecedenciaMaxima = 1
        physical_space.save()
        form = self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'A', '15/07/9999', True, '22/07/9999', '00:01', '00:02', physical_space, no_permission_user, mon=True)
        self.assertIs(form.is_valid(), False)
        physical_space.antecedenciaMaxima = 0
        physical_space.save()
        equipment.antecedenciaMaxima = 1
        equipment.save()
        form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'A', '15/07/9999', True, '22/07/9999', '00:01', '00:02', equipment, no_permission_user, mon=True)

        self.assertIs(form.is_valid(), False)
        equipment.antecedenciaMaxima = 0
        equipment.save()
        service.antecedenciaMaxima = 1
        service.save()
        form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'A', '15/07/9999', True, '22/07/9999', '00:01', '00:02', service, no_permission_user, mon=True)
        self.assertIs(form.is_valid(), False)
        service.antecedenciaMaxima = 0
        service.save()
        print('--MAX ADVANCE RESERVE IN RECURRENT TEST PASSED')

        print '--TESTING RECURRENT WITH NO WEEK DAY SELECTED'
        form = self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'A', '24/06/9999', True, '23/06/9999', '00:01', '00:02', physical_space, no_permission_user)
        self.assertIs(form.is_valid(), False)
        form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'A', '24/06/9999', True, '23/06/9999', '00:01', '00:02', equipment, no_permission_user)
        self.assertIs(form.is_valid(), False)
        form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'A', '24/06/9999', True, '23/06/9999', '00:01', '00:02', service, no_permission_user)
        self.assertIs(form.is_valid(), False)
        print '--RECURRENT WITH NO WEEK DAY SELECTED TEST PASSED'


        #clean database for next tests
        ReservaEquipamento.objects.all().delete()
        ReservaEspacoFisico.objects.all().delete()
        ReservaServico.objects.all().delete()
        ReservaRecorrente.objects.all().delete()

    def model_clean_tests(self, user, responsable, physical_space, equipment, service, unit):
        self.unit_clean_test()
        self.reserve_clean_test(user, responsable, physical_space, equipment, service)
        self.reservable_clean_test(unit)

    def reservable_clean_test(self, unit):
        # fotoLink must be an image
        print('--TESTING RESERVABLE IMAGELINK')
        physical_space = EspacoFisico.objects.create(nome='b', descricao='d', unidade=unit, localizacao='a', capacidade=1, fotoLink='http://www.pudim.com.br/pudim.jpg')
        try:
            physical_space.clean()
        except:
            self.fail('EspacoFisico.clean() raised an exception unexpectedly!')
        physical_space.delete()
        physical_space = EspacoFisico.objects.create(nome='b', descricao='d', unidade=unit, localizacao='a', capacidade=1, fotoLink='http://www.pudim.com.br/')
        self.assertRaises(ValidationError, lambda: physical_space.clean())
        physical_space.delete()

        equipment = Equipamento.objects.create(nome='b', descricao='d', unidade=unit, localizacao='a', patrimonio=1, fotoLink='http://www.pudim.com.br/pudim.jpg')
        try:
            equipment.clean()
        except:
            self.fail('Equipamento.clean() raised an exception unexpectedly!')
        equipment.delete()
        equipment = Equipamento.objects.create(nome='b', descricao='d', unidade=unit, localizacao='a', patrimonio=1, fotoLink='http://www.pudim.com.br/')
        self.assertRaises(ValidationError, lambda: equipment.clean())
        equipment.delete()

        service = Servico.objects.create(nome='b', descricao='d', unidade=unit, localizacao='a', fotoLink='http://www.pudim.com.br/pudim.jpg')
        try:
            service.clean()
        except:
            self.fail('Servico.clean() raised an exception unexpectedly!')
        service.delete()
        service = Equipamento.objects.create(nome='b', descricao='d', unidade=unit, localizacao='a', patrimonio=1, fotoLink='http://www.pudim.com.br/')
        self.assertRaises(ValidationError, lambda: service.clean())
        service.delete()
        print('--RESERVABLE IMAGELINK TEST PASSED')

    def unit_clean_test(self):
        # unit cannot have space in initials
        print('--TESTING UNIT WITH SPACE IN INITIALS')
        unit = Unidade.objects.create(sigla='initials with space', nome='a', descricao='d')
        self.assertRaises(ValidationError, lambda: unit.clean())
        unit.delete()
        print('--UNIT WITH SPACE IN INITIALS TEST PASSED')

        # logoLink must be an image
        print('--TESTING UNIT LOGOLINK')
        unit = Unidade.objects.create(sigla='a', nome='a', descricao='d', logoLink='http://www.pudim.com.br/pudim.jpg')
        try:
            unit.clean()
        except:
            self.fail('unit.clean() raised an exception unexpectedly!')
        unit.delete()
        unit = Unidade.objects.create(sigla='initials with space', nome='a', descricao='d', logoLink='http://www.pudim.com.br/')
        self.assertRaises(ValidationError, lambda: unit.clean())
        unit.delete()
        print('--UNIT LOGOLINK TEST PASSED')

    def unit_form_test(self, unit, no_permission_user):
        # while editing a form, user must be able to see parent unit even if he doesnt have permission
        print('--TESTING EDIT UNIT FORM')
        temp_unit = Unidade.objects.create(sigla='tem_pru', nome='temp_unit', unidadePai=unit, descricao='test')
        temp_unit.responsavel.add(no_permission_user)
        temp_unit.save()
        request.user = no_permission_user
        kwargs = dict()
        kwargs['request'] = request
        form = UnidadeAdminForm(**kwargs)
        father_unit_query = form.fields['unidadePai'].queryset
        self.assertEqual(1, len(father_unit_query))
        kwargs['request'] = request
        kwargs['instance'] = temp_unit
        form = UnidadeAdminForm(**kwargs)
        father_unit_query = form.fields['unidadePai'].queryset
        self.assertEqual(2, len(father_unit_query))
        temp_unit.delete()
        print('--EDITING UNIT FORM TEST PASSED')

    def group_only_test(self, responsable, permission_user, no_permission_user, physical_space, equipment, service):
        print '--TESTING GROUP ONLY'
        physical_space.somenteGrupo = True
        group = Group.objects.get(name='group')
        physical_space.grupos.add(group)
        physical_space.save()
        try:
            self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', physical_space, responsable, starting_reservable=True)
        except:
            self.fail('somenteGrupo flag raising error unexpectedly!')
        try:
            self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', physical_space, permission_user, starting_reservable=True)
        except:
            self.fail('somenteGrupo flag raising error unexpectedly!')
        self.assertRaises(PermissionDenied, lambda: self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', physical_space, no_permission_user, starting_reservable=True))
        physical_space.somenteGrupo = False
        physical_space.grupos.remove(group)
        physical_space.save()

        equipment.somenteGrupo = True
        equipment.grupos.add(group)
        equipment.save()
        try:
            form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', equipment, responsable, starting_reservable=True)
        except:
            self.fail('somenteGrupo flag raising error unexpectedly!')
        try:
            form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', equipment, permission_user, starting_reservable=True)
        except:
            self.fail('somenteGrupo flag raising error unexpectedly!')
        self.assertRaises(PermissionDenied, lambda: self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', equipment, no_permission_user, starting_reservable=True))
        equipment.somenteGrupo = False
        equipment.grupos.remove(group)
        equipment.save()

        service.somenteGrupo = True
        service.grupos.add(group)
        service.save()
        try:
            form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', service, responsable, starting_reservable=True)
        except:
            self.fail('somenteGrupo flag raising error unexpectedly!')
        try:
            form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', service, permission_user, starting_reservable=True)
        except:
            self.fail('somenteGrupo flag raising error unexpectedly!')
        self.assertRaises(PermissionDenied, lambda: self.create_form(ReservaServico, ReservaServicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', service, no_permission_user, starting_reservable=True))
        service.somenteGrupo = False
        service.grupos.remove(group)
        service.save()

    def status_options_test(self, responsable, permission_user, no_permission_user, physical_space, equipment, service):
        print '-- TESTING STATUS OPTION ON FORM'
        form = self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', physical_space, no_permission_user)
        reserve = form.save()
        editting_form = self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', physical_space, responsable, instance=reserve)
        self.assertEqual(4, len(editting_form.fields['estado'].choices))
        editting_form = self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', physical_space, no_permission_user, instance=reserve)
        self.assertEqual(2, len(editting_form.fields['estado'].choices))
        editting_form = self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', physical_space, permission_user, instance=reserve)
        self.assertEqual(2, len(editting_form.fields['estado'].choices))
        editting_form = self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'C', '18/06/9999', False, None, '00:01', '00:02', physical_space, responsable, instance=reserve)
        reserve = editting_form.save()
        editting_form = self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'C', '18/06/9999', False, None, '00:01', '00:02', physical_space, no_permission_user, instance=reserve)
        self.assertEqual(1, len(editting_form.fields['estado'].choices))
        editting_form = self.create_form(ReservaEspacoFisico, ReservaEspacoFisicoAdminForm, 'C', '18/06/9999', False, None, '00:01', '00:02', physical_space, permission_user, instance=reserve)
        self.assertEqual(1, len(editting_form.fields['estado'].choices))

        form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', equipment, no_permission_user)
        reserve = form.save()
        editting_form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', equipment, responsable, instance=reserve)
        self.assertEqual(4, len(editting_form.fields['estado'].choices))
        editting_form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', equipment, no_permission_user, instance=reserve)
        self.assertEqual(2, len(editting_form.fields['estado'].choices))
        editting_form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', equipment, permission_user, instance=reserve)
        self.assertEqual(2, len(editting_form.fields['estado'].choices))
        editting_form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'C', '18/06/9999', False, None, '00:01', '00:02', equipment, responsable, instance=reserve)
        reserve = editting_form.save()
        editting_form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'C', '18/06/9999', False, None, '00:01', '00:02', equipment, no_permission_user, instance=reserve)
        self.assertEqual(1, len(editting_form.fields['estado'].choices))
        editting_form = self.create_form(ReservaEquipamento, ReservaEquipamentoAdminForm, 'C', '18/06/9999', False, None, '00:01', '00:02', equipment, permission_user, instance=reserve)
        self.assertEqual(1, len(editting_form.fields['estado'].choices))

        form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', service, no_permission_user)
        reserve = form.save()
        editting_form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', service, responsable, instance=reserve)
        self.assertEqual(4, len(editting_form.fields['estado'].choices))
        editting_form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', service, no_permission_user, instance=reserve)
        self.assertEqual(2, len(editting_form.fields['estado'].choices))
        editting_form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'E', '18/06/9999', False, None, '00:01', '00:02', service, permission_user, instance=reserve)
        self.assertEqual(2, len(editting_form.fields['estado'].choices))
        editting_form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'C', '18/06/9999', False, None, '00:01', '00:02', service, responsable, instance=reserve)
        reserve = editting_form.save()
        editting_form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'C', '18/06/9999', False, None, '00:01', '00:02', service, no_permission_user, instance=reserve)
        self.assertEqual(1, len(editting_form.fields['estado'].choices))
        editting_form = self.create_form(ReservaServico, ReservaServicoAdminForm, 'C', '18/06/9999', False, None, '00:01', '00:02', service, permission_user, instance=reserve)
        self.assertEqual(1, len(editting_form.fields['estado'].choices))

        ReservaEspacoFisico.objects.all().delete()
        ReservaEquipamento.objects.all().delete()
        ReservaServico.objects.all().delete()

        print '--STATUS OPTION ON FORM TEST PASSED'

    def reserve_clean_test(self, user, responsable, physical_space, equipment, service):
        default_date = datetime.strptime('01/01/9999', '%d/%m/%Y').date()
        default_starting_time = datetime.strptime('00:01', '%H:%M').time()
        default_ending_time = datetime.strptime('00:02', '%H:%M').time()
        activitie = Atividade.objects.all()[0]

        # cannot make reserve in past days
        print('--TESTING RESERVE IN PAST DAYS')
        past_date = datetime.strptime('01/01/0001', '%d/%m/%Y').date()
        reserve = ReservaEspacoFisico.objects.create(data=past_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=physical_space)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaEquipamento.objects.create(data=past_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=equipment)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaServico.objects.create(data=past_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=service)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        print('--RESERVE IN PAST DAYS TEST PASSED')

        # ending time has to be after starting time
        print('--TESTING ENDING TIME AFTER STARTING TIME')
        error_ending_time = datetime.strptime('00:00', '%H:%M').time()
        reserve = ReservaEspacoFisico.objects.create(data=default_date, horaInicio=default_starting_time, horaFim=error_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=physical_space)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaEquipamento.objects.create(data=default_date, horaInicio=default_starting_time, horaFim=error_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=equipment)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaServico.objects.create(data=default_date, horaInicio=default_starting_time, horaFim=error_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=service)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        print('--ENDING TIME AFTER STARTING TIME TEST PASSED')

        # Test blocked reservable, user cannot reserve
        print('--TESTING BLOCKED RESERVABLE RESERVE TEST')
        physical_space.bloqueado = True
        equipment.bloqueado = True
        service.bloqueado = True
        reserve = ReservaEspacoFisico.objects.create(data=default_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=physical_space)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaEquipamento.objects.create(data=default_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=equipment)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaServico.objects.create(data=default_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=service)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        # responsable can reserve
        reserve = ReservaEspacoFisico.objects.create(data=default_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=responsable, ramal=0, finalidade='w', locavel=physical_space)
        try:
            reserve.clean()
        except:
            self.fail('reserve.clean() raised an exception unexpectedly!')
        reserve.delete()
        reserve = ReservaEquipamento.objects.create(data=default_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=responsable, ramal=0, finalidade='w', locavel=equipment)
        try:
            reserve.clean()
        except:
            self.fail('reserve.clean() raised an exception unexpectedly!')
        reserve.delete()
        reserve = ReservaServico.objects.create(data=default_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=responsable, ramal=0, finalidade='w', locavel=service)
        try:
            reserve.clean()
        except:
            self.fail('reserve.clean() raised an exception unexpectedly!')
        reserve.delete()
        equipment.bloqueado = False
        physical_space.bloqueado = False
        service.bloqueado = False
        print('--BLOCKED RESERVABLE RESERVE TEST PASSED')

        # Test advance max reserves
        print('--TESTING MAX ADVANCE')
        distant_date = default_date
        physical_space.antecedenciaMaxima = 1
        equipment. antecedenciaMaxima = 1
        service.antecedenciaMaxima = 1
        reserve = ReservaEspacoFisico.objects.create(data=distant_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=physical_space)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaEquipamento.objects.create(data=distant_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=equipment)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaServico.objects.create(data=distant_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=service)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaEspacoFisico.objects.create(data=distant_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=responsable, ramal=0, finalidade='w', locavel=physical_space)
        try:
            reserve.clean()
        except:
            self.fail('reserve.clean() raised an exception unexpectedly!')
        reserve.delete()
        reserve = ReservaEquipamento.objects.create(data=distant_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=responsable, ramal=0, finalidade='w', locavel=equipment)
        try:
            reserve.clean()
        except:
            self.fail('reserve.clean() raised an exception unexpectedly!')
        reserve.delete()
        reserve = ReservaServico.objects.create(data=distant_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=responsable, ramal=0, finalidade='w', locavel=service)
        try:
            reserve.clean()
        except:
            self.fail('reserve.clean() raised an exception unexpectedly!')
        reserve.delete()
        physical_space.antecedenciaMaxima = 0
        equipment.antecedenciaMaxima = 0
        service.antecedenciaMaxima = 0
        print('--MAX ADVANCE TEST PASSED')

        # Test min advance reserves
        print('--TESTING MIN ADVANCE')
        physical_space.antecedenciaMinima = 1
        equipment.antecedenciaMinima = 1
        service.antecedenciaMinima = 1
        error_date = datetime.today().date()
        reserve = ReservaEspacoFisico.objects.create(data=error_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=physical_space)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaEquipamento.objects.create(data=error_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=equipment)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaServico.objects.create(data=error_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=service)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaEspacoFisico.objects.create(data=error_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=responsable, ramal=0, finalidade='w', locavel=physical_space)
        try:
            reserve.clean()
        except:
            self.fail('reserve.clean() raised an exception unexpectedly!')
        reserve.delete()
        reserve = ReservaEquipamento.objects.create(data=error_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=responsable, ramal=0, finalidade='w', locavel=equipment)
        try:
            reserve.clean()
        except:
            self.fail('reserve.clean() raised an exception unexpectedly!')
        reserve.delete()
        reserve = ReservaServico.objects.create(data=error_date, horaInicio=default_starting_time, horaFim=default_ending_time, atividade=activitie, usuario=responsable, ramal=0, finalidade='w', locavel=service)
        try:
            reserve.clean()
        except:
            self.fail('reserve.clean() raised an exception unexpectedly!')
        reserve.delete()
        physical_space.antecedenciaMinima = 0
        equipment.antecedenciaMinima = 0
        service.antecedenciaMinima = 0
        print('--MIN ADVANCE TEST PASSED')

        # Test for datetime conflict, 5 cases
        print('--TESTING DATETIME CONFLICT')
        conflict_starting_time = datetime.strptime('08:00', '%H:%M').time()
        conflict_ending_time = datetime.strptime('10:00', '%H:%M').time()
        conflict_physical_space_reserve = ReservaEspacoFisico.objects.create(estado='A', data=default_date, horaInicio=conflict_starting_time, horaFim=conflict_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=physical_space)
        conflict_equipment_reserve = ReservaEquipamento.objects.create(estado='A', data=default_date, horaInicio=conflict_starting_time, horaFim=conflict_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=equipment)
        conflict_service_reserve = ReservaServico.objects.create(estado='A', data=default_date, horaInicio=conflict_starting_time, horaFim=conflict_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=service)
        # Case 1
        error_starting_time = (datetime.combine(datetime.today().date(), conflict_starting_time) - timedelta(hours=1)).time()
        error_ending_time = (datetime.combine(datetime.today().date(), conflict_starting_time) + timedelta(hours=1)).time()
        reserve = ReservaEspacoFisico.objects.create(data=default_date, horaInicio=error_starting_time, horaFim=error_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=physical_space)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaEquipamento.objects.create(data=default_date, horaInicio=error_starting_time, horaFim=error_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=equipment)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaServico.objects.create(data=default_date, horaInicio=error_starting_time, horaFim=error_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=service)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        # Case 2
        error_starting_time = (datetime.combine(datetime.today().date(), conflict_starting_time) + timedelta(hours=1)).time()
        error_ending_time = conflict_ending_time
        reserve = ReservaEspacoFisico.objects.create(data=default_date, horaInicio=error_starting_time, horaFim=error_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=physical_space)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaEquipamento.objects.create(data=default_date, horaInicio=error_starting_time, horaFim=error_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=equipment)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaServico.objects.create(data=default_date, horaInicio=error_starting_time, horaFim=error_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=service)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        # Case 3
        error_starting_time = conflict_starting_time
        error_ending_time = conflict_ending_time
        reserve = ReservaEspacoFisico.objects.create(data=default_date, horaInicio=error_starting_time, horaFim=error_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=physical_space)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaEquipamento.objects.create(data=default_date, horaInicio=error_starting_time, horaFim=error_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=equipment)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaServico.objects.create(data=default_date, horaInicio=error_starting_time, horaFim=error_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=service)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        # Case 4
        error_starting_time = (datetime.combine(datetime.today().date(), conflict_starting_time) - timedelta(hours=1)).time()
        error_ending_time = (datetime.combine(datetime.today().date(), conflict_starting_time) + timedelta(hours=1)).time()
        reserve = ReservaEspacoFisico.objects.create(data=default_date, horaInicio=error_starting_time, horaFim=error_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=physical_space)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaEquipamento.objects.create(data=default_date, horaInicio=error_starting_time, horaFim=error_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=equipment)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaServico.objects.create(data=default_date, horaInicio=error_starting_time, horaFim=error_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=service)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        # Case 5
        error_starting_time = (datetime.combine(datetime.today().date(), conflict_ending_time) - timedelta(hours=1)).time()
        error_ending_time = (datetime.combine(datetime.today().date(), conflict_ending_time) + timedelta(hours=1)).time()
        reserve = ReservaEspacoFisico.objects.create(data=default_date, horaInicio=error_starting_time, horaFim=error_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=physical_space)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaEquipamento.objects.create(data=default_date, horaInicio=error_starting_time, horaFim=error_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=equipment)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        reserve = ReservaServico.objects.create(data=default_date, horaInicio=error_starting_time, horaFim=error_ending_time, atividade=activitie, usuario=user, ramal=0, finalidade='w', locavel=service)
        self.assertRaises(ValidationError, lambda: reserve.clean())
        reserve.delete()
        print('--DATETIME CONFLICT TEST PASSED')