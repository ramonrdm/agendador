from django.contrib.auth.models import User, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def set_new_user_group(sender,instance,**kwargs):
    instance.is_staff = True
    group, group_created = Group.objects.get_or_create(name='pode reservar')
    if group_created:
        add_physical_space_reserve = Permission.objects.filter(codename='add_reservaespacofisico')
        for permission in add_physical_space_reserve:
            group.permissions.add(permission)
        change_physical_space_reserve = Permission.objects.filter(codename='change_reservaespacofisico')
        for permission in change_physical_space_reserve:
            group.permissions.add(permission)
        delete_physical_space_reserve = Permission.objects.filter(codename='delete_reservaespacofisico')
        for permission in delete_physical_space_reserve:
            group.permissions.add(permission)

        # equipment permissions
        add_equipment_reserve = Permission.objects.filter(codename='add_reservaequipamento', name='Can add reserva equipamento')
        for permission in add_equipment_reserve:
            group.permissions.add(permission)
        change_equipment_reserve = Permission.objects.filter(codename='change_reservaequipamento', name='Can change reserva equipamento')
        for permission in change_equipment_reserve:
            group.permissions.add(permission)
        delete_equipment_reserve = Permission.objects.filter(codename='delete_reservaequipamento', name='Can delete reserva equipamento')
        for permission in delete_equipment_reserve:
            group.permissions.add(permission)

        # services permissions
        add_service_reserve = Permission.objects.filter(codename='add_reservaservico')
        for permission in add_service_reserve:
            group.permissions.add(permission)
        change_service_reserve = Permission.objects.filter(codename='change_reservaservico')
        for permission in change_service_reserve:
            group.permissions.add(permission)
        delete_service_reserve = Permission.objects.filter(codename='delete_reservaservico')
        for permission in delete_service_reserve:
            group.permissions.add(permission)
    group.user_set.add(instance)
    group.save()
