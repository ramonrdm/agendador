# -*- coding: utf-8 -*-
import re
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import Widget, Select, MultiWidget, CheckboxInput
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib.admin import widgets
from django import forms
from datetime import datetime

class FilteredSelectMultipleJs(FilteredSelectMultiple):
    class Media():
        js = ('agenda/js/filtered_select_multiple.js',)
        css = {
            'all': ('agenda/css/filtered_select_multiple.css',),
        }

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
        label = name
        if 'label' in self.attrs:
            label = self.attrs['label']
        if value:
            try:
                initial = value.strftime('%H:%M')
            except:
                initial = datetime.strptime(value, '%H:%M').strftime('%H:%M')
        return render_to_string('agenda/widgets/select_time.html', dict(name=name, attrs=self.attrs, initial=initial, label=label))

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
        label = name
        if 'label' in self.attrs:
            label = self.attrs['label']
        try:
            initial = self.model.objects.get(id=value)
        except:
            initial = None
        return render_to_string('agenda/widgets/autocomplete.html', dict(name=name, query=self.query, attrs=self.attrs, initial=initial, label=label))

class ReadOnlyWidget(Widget):
    def __init__(self, search_model=None, check_box=False, check_box_value=None, attrs=None):
        self.attrs = attrs or {}
        self.search_model = search_model
        self.check_box = check_box
        self.check_box_value = check_box_value

    class Media():
        css = {
            'all': ('agenda/css/read_only.css',),
        }

    def render(self, name, value=None, attrs=None):
        model_field = False
        item_id = 0
        label = name
        if 'label' in self.attrs:
            label = self.attrs['label']
        try:
            value = datetime.strftime(value, '%d/%m/%Y')
        except:
            pass
        if self.search_model:
            item_id = value
            value = self.search_model.objects.get(id=value)
            model_field = True
        return render_to_string('agenda/widgets/read_only.html', dict(name=name, attrs=self.attrs, initial=value, model_field=model_field, item_id = item_id, check_box=self.check_box, check_box_value=self.check_box_value, label=label))

class RecurrentReserveWidget(CheckboxInput):

    class Media():
        js = ('agenda/js/recurrent_reserve.js',)