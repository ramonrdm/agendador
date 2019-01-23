from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from material.frontend import urls as frontend_urls
from agenda import views
from django_cas_ng import views as views2
from django.views import generic
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = [
    # url(r'^accounts/login/$', views2.login, name="cas_ng_login"),
    # url(r'^accounts/logout/$', views2.logout, name="cas_ng_logout"),
    # url(r'^admin/login/$', views2.login, name="cas_ng_login"),
    # url(r'^accounts/login/', views.manutencao, name="cas_ng_login"),
    url(r'^accounts/login/', auth_views.login, {"template_name":"agenda/login.html"}, name="login_normal"),
    url(r"^accounts/logout1/", auth_views.logout, name="logout_normal"),
    url(r'^accounts/register/', views.normal_registration, name="register_normal"),
    url(r'^accounts/logincas/', views.manutencao, name="cas_ng_login"),
    url(r'^accounts/logout/', views.manutencao, name="cas_ng_logout"),
    url(r'^accounts/resetpwrequest/$', views.reset_pw_request, name="reset_password_request"),
    url(r'^accounts/resetpw/(?P<token>\w+)/', views.reset_pw, name="reset_password"),
    #url(r'^admin/login/', views.manutencao, name="cas_ng_login"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(frontend_urls)),
    url(r'^$', views.index, name="index"),
    url(r'^$', views.index, name='Reservas UFSC'),
    url(r'^sobre$', views.sobre, name="sobre"),
    url(r'^espacos/$', views.espacos, name='espacos'),
    url(r'^equipamentos/$', views.equipamentos, name='equipamentos'),
    url(r"^mes/(e|f|s)/(\d+)/(\d+)/(\d+)/(prev|next)/$", views.mes, name="mes"),
    url(r"^mes/(e|f|s)/(\d+)/(\d+)/(\d+)/$", views.mes, name="mes"),
    url(r'^mes/(e|f|s)/(\d+)/$', views.mes, name='mes'),
    url(r"^mes/$", views.mes, name="mes"),
    url(r"^dia/(\d+)/(\d+)/(\d+)/(\d+)/$", views.dia, name="dia"),
    url(r'^ano/(\d+)/$', views.ano, name='ano'),
    url(r'^ano/(\d+)/(\d+)/$', views.ano, name='ano'),
    url(r'^ano/', views.ano, name='ano'),
    url(r'^(?P<unidade>[\w\.%+-]+)$', views.index, name='Reservas-UFSC'),
    url(r'^reservar/$', views.intermediaria, name="intermediaria"),
    url(r'^locavel/(e|f|s)/(\d+)/$', views.locavel, name='locavel'),
    url(r'^filtro_locavel_disponivel/(\d+)/(e|f|s)/(\w+)/(\w+)/(\w+)/', views.filtroLocavelDisponivel, name='resultado'),
    url(r'^get_atividade_set/$', views.get_atividade_set, name='get_atividade_set'),
    url(r'^get_pending_reserves/$', views.get_pending_reserves, name='get_pending_reserves'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^calendar/(?P<year>[\d]+)/(?P<month>[\d]+)/(?P<day>[\d]+)/$', views._calendar,name='cute_calendar'),
    # IDK what this do, but name was conflicting with month calendar
    url(r"^calendar/(e|f|s)/(\d+)/(\d+)/(\d+)/(prev|next)/$", views._calendar, name="cute_calendar_"),
    url(r"^calendar/(e|f|s)/(\d+)/(\d+)/(\d+)/$", views._calendar, name="cute_calendar__"),
    url(r'^calendar/(e|f|s)/(\d+)/$', views._calendar, name='cute_calendar___'),
    #dia, mes, ano,

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
