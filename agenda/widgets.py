# -*- coding: utf-8 -*-
import re
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import Widget, Select, MultiWidget
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib.admin import widgets
from datetime import datetime

class SelectTimeWidget(Widget):
    
    def __init__(self, attrs=None):
        self.attrs = attrs or {}

    class Media():
        css = {
            'all': ('agenda/css/select_time.css',),
        }
        js = ('material/js/jquery.datetimepicker.full.js', 'agenda/js/time_options.js',)

    def render(self, name, value, attrs=None):
        initial = None
        if value:
            try:
                initial = value.strftime('%H:%M')
            except:
                initial = datetime.strptime(value, '%H:%M').strftime('%H:%M')
        return render_to_string('agenda/select_time.html', dict(name=name, attrs=self.attrs, initial=initial))

class SelectDateWidget(Widget):

    def __init__(self, attrs=None):
        self.attrs = attrs or {}

    class Media():
        js = ('material/js/jquery.datetimepicker.full.js', 'agenda/js/date.js',)

    def render(self, name, value, attrs=None):
        if value:
            try:
                inp='<input class="date_picker validate" data-lang="pt-br" id="id_'+name+'" name="'+name+'" type="text" value="'+value.strftime('%d/%m/%Y')+'">'
            except:
                inp='<input class="date_picker validate" data-lang="pt-br" id="id_'+name+'" name="'+name+'" type="text" value="'+datetime.strptime(value, '%d/%m/%Y').strftime('%d/%m/%Y')+'">'
        else:
            inp='<input class="date_picker validate" data-lang="pt-br" id="id_'+name+'" name="'+name+'" type="text">'
        label='<label for="id_'+name+'">'+name.title()+'</label>'
        output = '<div class="input-field">' + inp + label + '</div>'
        return output

class DynamicAtividadeWidget(widgets.RelatedFieldWidgetWrapper):
    class Media():
        js = ('agenda/js/dynamic_atividade.js',)

class AutocompleteWidget(Widget):
    def __init__(self, query, model, attrs=None):
        self.attrs = attrs or {}
        self.query = query
        self.model = model

    class Media():
        css = {
            'all': ('agenda/css/autocomplete.css',),
        }
        js = ('material/js/materialize.js', 'agenda/js/autocomplete.js',)

    def render(self, name, value, attrs=None):
        try:
            initial = self.model.objects.get(id=value)
        except:
            initial = None
        return render_to_string('agenda/autocomplete.html', dict(name=name, query=self.query, attrs=self.attrs, initial=initial))