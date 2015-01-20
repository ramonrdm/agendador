from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'agendador.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'agenda.views.index', name='index'),
    url(r'^requisitos', 'agenda.views.sobre', name='requisitos'),
    url(r'^espacos/$', 'agenda.views.espacos', name='espacos'),
    #url(r'^calendar/(\d+)/(\d+)', 'agenda.views.calendar', name='calendar'),
    url(r"^month/(\d+)/(\d+)/(\d+)/(prev|next)/$", "agenda.views.month"),
    url(r"^month/(\d+)/(\d+)/(\d+)/$", "agenda.views.month"),
    url(r"^month$", "agenda.views.month"),
    url(r"^dia/(\d+)/(\d+)/(\d+)/(\d+)/$", "agenda.views.dia"),
    #url(r"^settings/$", "agenda.views.settings"),
    url(r'^main/(\d+)/$', "agenda.views.main", name='main'),
    url(r'^main/(\d+)/(\d+)/$', "agenda.views.main", name='main'),
    url(r'^main/', "agenda.views.main", name='main'),
    url(r'^addreserva/', "agenda.views.addreserva", name='addreserva'),
    (r'^accounts/login/', 'django_cas_ng.views.login'),
    (r'^accounts/logout$', 'django_cas_ng.views.logout'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
