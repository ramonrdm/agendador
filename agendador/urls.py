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
    #url(r'^accounts/login/$', views2.login, name="cas_ng_login"),
    #url(r'^accounts/logout/$', views2.logout, name="cas_ng_logout"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(frontend_urls)),
    url(r'^$', views.index, name="index"),
    url(r'^$', views.index, name='Reservas UFSC'),
    url(r'^sobre$', views.sobre, name="sobre"),
    url(r'^espacos/$', views.espacos, name='espacos'),
    url(r'^equipamentos/$', views.equipamentos, name='equipamentos'),
    url(r"^mes/(e|f|s)/(\d+)/(\d+)/(\d+)/(prev|next)/$", views.mes, name="mes"),
    url(r"^mes/(e|f|s)/(\d+)/(\d+)/(\d+)/$", views.mes, name="mes"),
    url(r"^mes/$", views.mes, name="mes"),
    url(r"^dia/(\d+)/(\d+)/(\d+)/(\d+)/$", views.dia, name="dia"),
    url(r'^ano/(\d+)/$', views.ano, name='ano'),
    url(r'^ano/(\d+)/(\d+)/$', views.ano, name='ano'),
    url(r'^ano/', views.ano, name='ano'),
    url(r'^addreserva/$', views.addreserva, name='addreserva'),
    url(r'^addreserva/(\d+)/$', views.addreserva, name='addreserva'),
    url(r'^addreserva/(\d+)/(\d+)/(\d+)/(\d+)/$', views.addreserva, name='addreserva'),
    url(r'^(?P<unidade>\w+)$', views.index, name='Reservas-UFSC'),
    url(r'^reservar/(?P<tipo>e|f|s)/(?P<id_equip>\d+)/(?P<data_numero>\d+)$', views.intermediaria, name="intermediaria"),
    url(r'^reservar/(?P<tipo>e|f|s)/(?P<id_equip>\d+)/(?P<data_numero>\d+)/(?P<horaInicio>\d+)/(?P<horaFim>)$', views.intermediaria, name="intermediaria"),
    url(r'^locavel/(e|f|s)/(\d+)/$', views.locavel, name='locavel'),
    url(r'^resultado/(e|f|s)/(\w+)/(\w+)/(\w+)/', views.resultado, name='resultado'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

