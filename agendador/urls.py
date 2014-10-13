from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'agendador.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'agenda.views.index', name='index'),
    url(r'^requisitos', 'agenda.views.sobre', name='requisitos'),
    #url(r'^calendar/(\d+)/(\d+)', 'agenda.views.calendar', name='calendar'),
    url(r"^month/(\d+)/(\d+)/(prev|next)/$", "agenda.views.month"),
    url(r"^month/(\d+)/(\d+)/$", "agenda.views.month"),
    url(r"^month$", "agenda.views.month"),
    url(r"^day/(\d+)/(\d+)/(\d+)/$", "agenda.views.day"),
    #url(r"^settings/$", "agenda.views.settings"),
    url(r'^main/(\d+)/$', "agenda.views.main", name='main'),
    url(r'^main/', "agenda.views.main", name='main'),    
)
