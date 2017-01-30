from django.apps import AppConfig
from material.frontend.apps import ModuleMixin

class AgendaConfig(ModuleMixin, AppConfig):
    name = 'agenda'
    icon = '<i class="material-icons">payment</i>'
    #icon = '<i class="material-icons">flight_takeoff</i>'