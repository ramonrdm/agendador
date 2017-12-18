import re
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import Widget, Select, MultiWidget
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from datetime import datetime

class SelectTimeWidget(Widget):
    
    def __init__(self, attrs=None):
        self.attrs = attrs or {}

    class Media():
		js = ('material/js/jquery.datetimepicker.full.js', 'agenda/js/time_options.js',)

    def render(self, name, value, attrs=None):
        if value:
            try:
                inp='<input class="ufsc_time validate" data-lang="pt-br" id="id_'+name+'" name="'+name+'" type="text" value="'+value.strftime('%H:%M')+'">'
            except:
                inp='<input class="ufsc_time validate" data-lang="pt-br" id="id_'+name+'" name="'+name+'" type="text" value="'+datetime.strptime(value, '%H:%M').strftime('%H:%M')+'">'
        else:
            inp='<input class="ufsc_time validate" data-lang="pt-br" id="id_'+name+'" name="'+name+'" type="text">'
    	label='<label for="id_'+name+'">'+name.title()+'</label>'
    	output = '<div class="input-field">' + inp + label + '</div>'
        return output

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
