from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from material.frontend import urls as frontend_urls
from agenda import views
from django_cas_ng import views as views2
from django.views import generic
admin.autodiscover()

urlpatterns = [
    #url('^$', generic.TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'^$', views.index, name="index"),
    url(r'^admin', include(admin.site.urls)),
    url(r'', include(frontend_urls)),
    url(r'^$', views.index, name='Reservas UFSC'),
    #url(r'^sobre$', views.Sobre2.as_view(template_name="agenda/sobre.html, content_type='text/plain'"), name='sobre'),
    url(r'^sobre$', views.sobre, name="sobre"),
    url(r'^espacos/$', views.espacos, name='espacos'),
    url(r'^equipamentos/$', views.equipamentos, name='equipamentos'),
    url(r"^mes/(\d+)/(\d+)/(\d+)/(prev|next)/$", views.mes, name="mes"),
    url(r"^mese/(\d+)/(\d+)/(\d+)/(prev|next)/$", views.mese, name="mese"),
    url(r"^mes/(\d+)/(\d+)/(\d+)/$", views.mes, name="mes"),
    url(r"^mese/(\d+)/(\d+)/(\d+)/$", views.mese, name="mese"),
    url(r"^mes/$", views.mes, name="mes"),
    url(r"^mese/$", views.mese, name="mese"),
    url(r"^dia/(\d+)/(\d+)/(\d+)/(\d+)/$", views.dia, name="dia"),
    url(r'^ano/(\d+)/$', views.ano, name='ano'),
    url(r'^ano/(\d+)/(\d+)/$', views.ano, name='ano'),
    url(r'^ano/', views.ano, name='ano'),
    url(r'^addreserva/$', views.addreserva, name='addreserva'),
    url(r'^addreserva/(\d+)/$', views.addreserva, name='addreserva'),
    url(r'^addreserva/(\d+)/(\d+)/(\d+)/(\d+)/$', views.addreserva, name='addreserva'),
    url(r'^accounts/login/$', views2.login, name="login cas"),
    url(r'^accounts/logout/$', views2.logout, name="logout cas"),
    url(r'^(?P<unidade>\w+)$', views.index, name='Reservas-UFSC'),
    url(r'^intermediaria/(?P<id_equip>\d+)/(?P<data_numero>\d+)$', views.intermediaria, name="intermediaria"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

