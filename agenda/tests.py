from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission

from .models import *

class AdminViewPermissionsTests(TestCase):
    def create_preset(self):
        # Create users with different prioritys
        # Also gives them all permissions and staff, so they can see admin page
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
        parentUnit = Unidade.objects.create(sigla='pu', nome='parent unit', responsavel=unit_responsable, descricao='test')
        parentUnit.save()
        childUnit = Unidade.objects.create(sigla='cu', nome='child unit', responsavel=sub_unit_responsable, unidadePai=parentUnit, descricao='test')
        parentUnit.save()

        # Create a space and a equipment for each user (except common)
        space0 = EspacoFisico.objects.create(nome='space1', descricao='test', responsavel=item_responsable, unidade=childUnit, capacidade=0)
        space0.save()
        equipment0 = Equipamento.objects.create(nome='equipmnet1', descricao='test', responsavel=item_responsable, unidade=childUnit, patrimonio=0)
        equipment0.save()
        space1 = EspacoFisico.objects.create(nome='space2', descricao='test', responsavel=sub_unit_responsable, unidade=childUnit, capacidade=0)
        space1.save()
        equipment1 = Equipamento.objects.create(nome='equipment2', descricao='test', responsavel=sub_unit_responsable, unidade=childUnit, patrimonio=0)
        equipment1.save()
        space2 = EspacoFisico.objects.create(nome='space3', descricao='test', responsavel=unit_responsable, unidade=childUnit, capacidade=0)
        space2.save()
        equipment2 = Equipamento.objects.create(nome='equipment3', descricao='test', responsavel=unit_responsable, unidade=childUnit, patrimonio=0)
        equipment2.save()

        # Create a activitie (required for reserve)
        activitie = Atividade.objects.create(nome='activitie', descricao='default')

        # Create a reserve for both space and equipment for each user
        reserve_space0 = ReservaEspacoFisico.objects.create(data='1000-10-10', horaInicio='00:00', horaFim='00:00', atividade=activitie, usuario=common, ramal=0, finalidade='t', espacoFisico=space0)
        reserve_space0.save()
        reserve_equipment0 = ReservaEquipamento.objects.create(data='1000-10-10', horaInicio='00:00', horaFim='00:00', atividade=activitie, usuario=common, ramal=0, finalidade='t', equipamento=equipment0)
        reserve_equipment0.save()
        reserve_space1 = ReservaEspacoFisico.objects.create(data='1000-10-10', horaInicio='00:00', horaFim='00:00', atividade=activitie, usuario=item_responsable, ramal=0, finalidade='t', espacoFisico=space1)
        reserve_space1.save()
        reserve_equipment1 = ReservaEquipamento.objects.create(data='1000-10-10', horaInicio='00:00', horaFim='00:00', atividade=activitie, usuario=item_responsable, ramal=0, finalidade='t', equipamento=equipment1)
        reserve_equipment1.save()
        reserve_space2 = ReservaEspacoFisico.objects.create(data='1000-10-10', horaInicio='00:00', horaFim='00:00', atividade=activitie, usuario=sub_unit_responsable, ramal=0, finalidade='t', espacoFisico=space2)
        reserve_space2.save()
        reserve_equipment2 = ReservaEquipamento.objects.create(data='1000-10-10', horaInicio='00:00', horaFim='00:00', atividade=activitie, usuario=sub_unit_responsable, ramal=0, finalidade='t', equipamento=equipment2)
        reserve_equipment2.save()

    def test_admin_view_filter(self):
        self.create_preset()
        c = Client()
        print c.login(username='superuser', password='a')
        response = c.get('/adminagenda/equipamento/')
        print response.status_code
        print response.content
