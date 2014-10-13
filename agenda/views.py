# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.utils.safestring import mark_safe
##
import time
import calendar
from datetime import date, datetime, timedelta

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.core.context_processors import csrf
from django.forms.models import modelformset_factory
from django.template import RequestContext

from agenda.models import *

mnames = "Janeiro Fevereiro Março Abril Maio Junho Julho Agosto Setembro Outubro Novembro Dezembro"
mnames = mnames.split()

# Create your views here.
def index(request):

	titulo = "Agendador de espaço físico do CCS"
	corpo = "Bem vindo ao Agendador de espaço físico do CCS"
	return render_to_response("index.html",{'corpo':corpo,"titulo":titulo})

def sobre(request):
	titulo = "Requisitos do Agendador CCS"
	return render_to_response("sobre.html", {'titulo':titulo})

# #calendario
# def calendar(request, year, month):
#   my_workouts = Workouts.objects.order_by('my_date').filter(
#     my_date__year=year, my_date__month=month
#   )
#   cal = WorkoutCalendar(my_workouts).formatmonth(year, month)
#   return render_to_response('my_template.html', {'calendar': mark_safe(cal),})

#@login_required
def main(request, year=None):
    """Main listing, years and months; three years per page."""
    # prev / next years
    if year: year = int(year)
    else:    year = time.localtime()[0]

    nowy, nowm = time.localtime()[:2]
    lst = []

    # create a list of months for each year, indicating ones that contain entries and current
    for y in [year, year+1, year+2]:
        mlst = []
        for n, month in enumerate(mnames):
            entry = current = False   # are there entry(s) for this month; current month?
            entries = Entry.objects.filter(date__year=y, date__month=n+1)
            #if not _show_users(request):
            #    entries = entries.filter(creator=request.user)

            if entries:
                entry = True
            if y == nowy and n+1 == nowm:
                current = True
            mlst.append(dict(n=n+1, name=month, entry=entry, current=current))
        lst.append((y, mlst))

    return render_to_response("main.html", dict(years=lst, user=request.user, year=year))

def month(request, year, month, change=None):
    """Listing of days in `month`."""
    year, month = int(year), int(month)

    # apply next / previous change
    if change in ("next", "prev"):
        now, mdelta = date(year, month, 15), timedelta(days=31)
        if change == "next":   mod = mdelta
        elif change == "prev": mod = -mdelta

        year, month = (now+mod).timetuple()[:2]

    # init variables
    cal = calendar.Calendar()
    month_days = cal.itermonthdays(year, month)
    nyear, nmonth, nday = time.localtime()[:3]
    lst = [[]]
    week = 0

    # make month lists containing list of days for each week
    # each day tuple will contain list of entries and 'current' indicator
    for day in month_days:
        entries = current = False   # are there entries for this day; current day?
        if day:
            entries = Entry.objects.filter(date__year=year, date__month=month, date__day=day)
            #if not _show_users(request):
            #    entries = entries.filter(creator=request.user)
            if day == nday and year == nyear and month == nmonth:
                current = True

        lst[week].append((day, entries, current))
        if len(lst[week]) == 7:
            lst.append([])
            week += 1

    return render_to_response("month.html", dict(year=year, month=month, user=request.user, month_days=lst, mname=mnames[month-1]))

def day(request):
	render_to_response("main.html")
