from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from material.frontend import urls as frontend_urls
from agenda import views
from django_cas_ng import views as views2
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^admin', include(admin.site.urls)),
    #url(r'', include(frontend_urls)),
    url(r'^$', views.index, name='Reservas UFSC'),
    url(r'^(?P<grupo>\w+)$', views.index, name='Reservas UFSC'),
    url(r'^sobre/$', views.sobre, name='Sobre'),
    url(r'^espacos/$', views.espacos, name='espacos'),
    url(r'^equipamentos/$', views.equipamentos, name='equipamentos'),
    url(r"^mes/(\d+)/(\d+)/(\d+)/(prev|next)/$", views.mes),
    url(r"^mes/(\d+)/(\d+)/(\d+)/$", views.mes),
    url(r"^mes/$", views.mes),
    url(r"^dia/(\d+)/(\d+)/(\d+)/(\d+)/$", views.dia),
    url(r'^ano/(\d+)/$', views.ano, name='ano'),
    url(r'^ano/(\d+)/(\d+)/$', views.ano, name='ano'),
    url(r'^ano/', views.ano, name='ano'),
    url(r'^addreserva/$', views.addreserva, name='addreserva'),
    url(r'^addreserva/(\d+)/$', views.addreserva, name='addreserva'),
    url(r'^addreserva/(\d+)/(\d+)/(\d+)/(\d+)/$', views.addreserva, name='addreserva'),
    url(r'^accounts/login/$', views2.login),
    url(r'^accounts/logout/$', views2.logout),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
