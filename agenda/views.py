# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.utils.safestring import mark_safe
import time, calendar
from datetime import date, datetime, timedelta
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotFound
from django.forms.models import modelformset_factory
from django.template import RequestContext, Library
from django.views.decorators import csrf
from agenda.models import *
from agenda.forms import ReservaEspacoFisicoAdminForm
from django import forms
from django.contrib.admin.sites import AdminSite
from datetime import date
import admin
from forms import *

from material.frontend.views import ModelViewSet

month_names = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
unidade_default = 'ufsc'

def index(request, unidade=unidade_default):
    if request.method == 'POST':
        search_form = SearchFilterForm(request.POST)
        if search_form.is_valid():
            data = search_form.cleaned_data['data'].strftime('%d%m%Y')
            horaInicio = search_form.cleaned_data['horaInicio'].strftime('%H%M')
            horaFim = search_form.cleaned_data['horaFim'].strftime('%H%M')
            tipo = search_form.cleaned_data['tipo']
            return redirect('/resultado/'+ tipo +'/' + data + '/' + horaInicio + '/' + horaFim + '/')
    else:
        search_f = SearchFilterForm(tipo='f')
        search_e = SearchFilterForm(tipo='e')
    #titulo = "Agendador UFSC"
    #corpo = "Bem vindo ao Agendador de espaços físicos e equipamentos da UFSC"

    try:
        unidade = Unidade.objects.get(sigla=unidade)
    except Unidade.DoesNotExist:
        try:
            unidade = Unidade.objects.get(sigla="UFSC")
        except Unidade.DoesNotExist:
            return render_to_response("agenda/index.html")
            
    
    unidades = Unidade.objects.filter(unidadePai=unidade)

    espacosFisicos = EspacoFisico.objects.filter(unidade=unidade).filter(visivel=True)
    equipamentos = Equipamento.objects.filter(unidade=unidade).filter(visivel=True)

    year = time.localtime()[0]
    current_year, current_month = time.localtime()[:2]
    lst = []
    # create a list of months for each year, indicating ones that contain entries and current
    for y in [year, year+1]:
        month_list = []
        for n, month in enumerate(month_names):
            if (n + 1) >= current_month or y != year:
                month_list.append(dict(n=n+1, name=month_names[n]))
        lst.append((y, month_list))


    return render(
        request,
        "agenda/index.html",
        dict(
            unidade=unidade, unidades=unidades,
            espacosfisicos=espacosFisicos, equipamentos=equipamentos,
            years=lst, user=request.user, search_f=search_f, search_e=search_e
            )
        )

def sobre(request):
	return render(request, "agenda/sobre.html")

def ano(request, unidade=None ,year=None):
    # prev / next years
    if year: year = int(year)
    else:    year = time.localtime()[0]
    nowy, nowm = time.localtime()[:2]
    lst = []
    # create a list of months for each year, indicating ones that contain entries and current
    for y in [year, year+1]:
        mlst = []
        for n, month in enumerate(month_names):
            entry = current = False
            if y == nowy and n+1 == nowm:
                current = True
            mlst.append(dict(n=n+1, name=month, current=current))
        lst.append((y, mlst))
    
    espacosfisicos = EspacoFisico.objects.filter(unidade=unidade)

    return render_to_response("ano.html", dict(years=lst, user=request.user, year=year, espacosfisicos=espacosfisicos))

def locavel(request, tipo=None, locavel=None):
    specific = dict()
    if tipo == 'e':
        locavel = Equipamento.objects.get(id=locavel)
        specific['patrimonio'] = locavel.patrimonio
    else:
        locavel = EspacoFisico.objects.get(id=locavel)
        specific['capacidade'] = locavel.capacidade
        atividadesPermitidas = locavel.atividadesPermitidas.all()
        atividades = list()
        for atividade in atividadesPermitidas:
            atividades.append(atividade.nome)
        specific['atividades permitidas'] = (", ").join(atividades)
    if not locavel.visivel:
        return HttpResponseNotFound()
    responsaveis = locavel.responsavel.all()
    grupo = locavel.grupo
    ret = request.META.get('HTTP_REFERER')
    return render(request, 'agenda/locavel.html', dict(tipo=tipo, locavel=locavel, responsaveis=responsaveis, grupo=grupo, specific=specific, ret=ret))

def mes(request, tipo=None, espaco=None, year=None, month=None, change=None):
    """Listing of days in `month`."""
    espaco, year, month = int(espaco), int(year), int(month)
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
    for day in month_days:
        entries = current = False
        if day:
            if tipo=="e":
                entries = ReservaEquipamento.objects.filter(data__year=year, data__month=month, data__day=day, locavel=espaco)
            else:
                entries = ReservaEspacoFisico.objects.filter(data__year=year, data__month=month, data__day=day, locavel=espaco)

        if day == nday and year == nyear and month == nmonth:
            current = True

        lst[week].append((day, entries, current))
        if len(lst[week]) == 7:
            lst.append([])
            week += 1
    if(tipo=="e"):
        espacofisico = Equipamento.objects.get(id=espaco)
    else:
        espacofisico = EspacoFisico.objects.get(id=espaco)
        tipo = 'f'
    return render(
            request,
            "agenda/mes.html", 
            dict(
                espaco=espacofisico, year=year, month=month, 
                user=request.user, month_days=lst, mname=month_names[month-1],
                tipo=tipo
                ))

def dia(request, espaco, year, month, day):
    """Entries for the day."""
    nyear, nmonth, nday = time.localtime()[:3]
    espacofisico = EspacoFisico.objects.get(id=espaco)
    reservas = ReservaEspacoFisico.objects.filter(data__year=year, data__month=month, data__day=day, espacoFisico=espaco).order_by("horaInicio")
    return render(request, "agenda/dia.html", dict(reservas=reservas, espaco=espacofisico, anovisualizacao=year ,mesvisualizacao=month, dia=day))


def espacos(request):
	espacos1 = EspacoFisico.objects.order_by("nome").all()
	ano = time.localtime()[0]
	mes = time.localtime()[1]
	return render(
            request,
            "agenda/espacos.html",
            dict(ano=ano, mes=mes, espacos=espacos1
                ))

def equipamentos(request):
    espacos1 = Equipamento.objects.order_by("nome").all()
    ano = time.localtime()[0]
    mes = time.localtime()[1]
    return render_to_response("espacos.html", {'ano': ano, 'mes': mes, 'espacos': espacos1})

def intermediaria(request):
    id_equip = request.GET['id']
    data_numero = request.GET['data']
    try:
        horaInicio = request.GET['horaInicio']
        horaFim = request.GET['horaFim']
    except:
        horaInicio = None
        horaFim = None
    request.session['id_equip'] = id_equip
    data_string = str(data_numero)
    print data_numero
    data = data_string[0]+data_string[1]+'/'+data_string[2]+data_string[3]+'/'+data_string[4]+data_string[5]+data_string[6]+data_string[7]
    request.session['data'] = data
    if horaInicio and horaFim:
        horaInicio = horaInicio[:2]+':'+horaInicio[2:]
        horaFim = horaFim[:2]+':'+horaFim[2:]
    request.session['horaInicio'] = horaInicio
    request.session['horaFim'] = horaFim
    data = {'success': True}
    return JsonResponse(data)

@login_required
def resultado(request, tipo, sData, sHoraInicio, sHoraFim):
    data = datetime.strptime(sData, '%d%m%Y')
    horaInicio = datetime.strptime(sHoraInicio, '%H%M').time()
    horaFim = datetime.strptime(sHoraFim, '%H%M').time()
    if tipo == 'f':
        ma = admin.EspacoFisicoAdmin(EspacoFisico, AdminSite())
        query = ma.get_queryset(request)
        reserves = ReservaEspacoFisico.objects.none()
        for espaco in query:
            reserves = reserves | espaco.reservaespacofisico_set.filter(data=data)
    if tipo == 'e':
        ma = admin.EquipamentoAdmin(Equipamento, AdminSite())
        query = ma.get_queryset(request)
        reserves = ReservaEquipamento.objects.none()
        for equipamento in query:
            reserves = reserves | equipamento.reservaequipamento_set.filter(data=data)

    for r in reserves:
        if  (
            (horaFim  > r.horaInicio and horaFim < r.horaFim) or 
            (horaInicio > r.horaInicio and horaInicio < r.horaFim ) or 
            (horaInicio == r.horaInicio and horaFim == r.horaFim) or
            (r.horaInicio > horaInicio and r.horaInicio < horaFim) or
            (horaInicio < r.horaFim < horaFim)
            ):
            query = query.exclude(id=r.locavel.id)
    return render(request, "agenda/search_result.html", dict(query=query, data=sData, horaInicio=sHoraInicio, horaFim=sHoraFim, tipo=tipo))

@login_required
def get_atividade_set(request):
    if request.method == 'POST':
        tipo = request.POST['title']
        locavel = request.POST['locavel']
        if 'espaco fisico' in tipo:
            locavel = EspacoFisico.objects.get(nome=locavel)
            ma = admin.EspacoFisicoAdmin(EspacoFisico, AdminSite())
        elif 'equipamento' in tipo:
            locavel = Equipamento.objects.get(nome=locavel)
            ma = admin.EquipamentoAdmin(Equipamento, AdminSite())
        query = ma.get_queryset(request)
        if locavel in query:
            atividades = locavel.atividadesPermitidas.all()
            n = list()
            i = list()
            for atividade in atividades:
                n.append(atividade.nome)
                i.append(atividade.id)
            data = {'atividades': n, 'ids': i}
            return JsonResponse(data)
    return HttpResponseNotFound()
