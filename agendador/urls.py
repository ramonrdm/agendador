from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from material.frontend import urls as frontend_urls
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin', include(admin.site.urls)),
    url(r'', include(frontend_urls)),
    url(r'^$', 'agenda.views.index', name='Reservas UFSC'),
    url(r'^sobre$', 'agenda.views.sobre', name='Sobre'),
    url(r'^espacos$', 'agenda.views.espacos', name='espacos'),
    url(r'^equipamentos$', 'agenda.views.equipamentos', name='equipamentos'),
    url(r"^mes/(\d+)/(\d+)/(\d+)/(prev|next)/$", "agenda.views.mes"),
    url(r"^mes/(\d+)/(\d+)/(\d+)/$", "agenda.views.mes"),
    url(r"^mes/$", "agenda.views.mes"),
    url(r"^dia/(\d+)/(\d+)/(\d+)/(\d+)/$", "agenda.views.dia"),
    url(r'^ano/(\d+)/$', "agenda.views.ano", name='ano'),
    url(r'^ano/(\d+)/(\d+)/$', "agenda.views.ano", name='ano'),
    url(r'^ano', "agenda.views.ano", name='ano'),
    url(r'^addreserva/$', "agenda.views.addreserva", name='addreserva'),
    url(r'^addreserva/(\d+)/$', "agenda.views.addreserva", name='addreserva'),
    url(r'^addreserva/(\d+)/(\d+)/(\d+)/(\d+)/$', "agenda.views.addreserva", name='addreserva'),
    url(r'^(?P<grupo>\w+)$', 'agenda.views.index', name='Reservas UFSC'),
    (r'^accounts/login/$', 'django_cas_ng.views.login'),
    (r'^accounts/logout/$', 'django_cas_ng.views.logout'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
