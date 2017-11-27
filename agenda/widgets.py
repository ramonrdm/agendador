from django.contrib.admin.widgets import AdminTimeWidget
from django.conf import settings
from django import forms
from django.contrib.staticfiles.templatetags.staticfiles import static

class CustomTimeWidget(forms.TimeInput):
    class Media:
        js = (static('agenda/js/time_options.js'),)
