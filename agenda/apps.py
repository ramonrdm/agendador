from django.apps import AppConfig
from material.frontend.apps import ModuleMixin

class AgendaConfig(ModuleMixin, AppConfig):
    name = 'agenda'
    icon = '<i class="material-icons">event_note</i>'