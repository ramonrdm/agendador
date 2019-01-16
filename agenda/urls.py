from django.views.generic import TemplateView
from django.conf.urls import url

urlpatterns = [
    url('^$', TemplateView.as_view(template_name="agenda/index.html"), name="index"),
    url('^calendar', TemplateView.as_view(template_name="agenda/calendar.html"), name="calendar"),
]
