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
from django.contrib.flatpages.models import FlatPage

from datetime import date
import admin
from forms import *

from material.frontend.views import ModelViewSet

month_names = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
unidade_default = 'ufsc'

def index(request, unidade=None):
    # get unit
    try:  # try to get given unit
        unidade = Unidade.objects.get(sigla__iexact=unidade)
    # no given unit. check if unit was given in the domain
    except Unidade.DoesNotExist:
        typed_url = request.build_absolute_uri()
        splitted_url = typed_url.split('.')
        unidade = None
        for url_part in splitted_url:  # check url for unit
            lower_root = unidade_default.lower()  # the programmer may have put uppercase in root. Lets avoid errors
            if url_part != lower_root:  # skip root unit, since it may be part of the domain
                try:
                    unidade = Unidade.objects.get(sigla__iexact=url_part)
                    break
                except:
                    pass  # url_part was not an unit. that's ok
        # no unit found
        if not unidade:
            try:
                unidade = Unidade.objects.get(sigla__iexact=unidade_default)  # get root unit
            except Unidade.DoesNotExist:
                return render_to_response("agenda/index.html")  # can't find unit to load. render blank

    if request.method == 'POST':
        search_form = SearchFilterForm(request.POST)
        if search_form.is_valid():
            data = search_form.cleaned_data['data'].strftime('%d%m%Y')
            horaInicio = search_form.cleaned_data['horaInicio'].strftime('%H%M')
            horaFim = search_form.cleaned_data['horaFim'].strftime('%H%M')
            tipo = search_form.cleaned_data['tipo']
            return redirect('/filtro_locavel_disponivel/' + str(unidade.id) + '/' + tipo +'/' + data + '/' + horaInicio + '/' + horaFim + '/')
        elif search_form.data['tipo'] == 'f':
            search_f = search_form
            search_e = SearchFilterForm(tipo='e')
        elif search_form.data['tipo'] == 'e':
            search_f = SearchFilterForm(tipo='f')
            search_e = search_form
    else:
        search_f = SearchFilterForm(tipo='f')
        search_e = SearchFilterForm(tipo='e')
    #titulo = "Agendador UFSC"
    #corpo = "Bem vindo ao Agendador de espaços físicos e equipamentos da UFSC"



    unidades = Unidade.objects.filter(unidadePai=unidade)

    espacosFisicos = EspacoFisico.objects.filter(unidade=unidade).filter(invisivel=False)
    equipamentos = Equipamento.objects.filter(unidade=unidade).filter(invisivel=False)

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

def redirect_to_calendar(request, reservable_type, reservable_id):
    today = datetime.today()
    year = today.year
    month = today.month
    return mes(request, reservable_type, reservable_id, year, month)

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
    if locavel.invisivel:
        return HttpResponseNotFound()
    responsaveis = locavel.responsavel.all()
    grupos = locavel.grupos.all()
    ret = request.META.get('HTTP_REFERER')
    url_to_reserves = request.build_absolute_uri() + 'reservas'
    return render(request, 'agenda/locavel.html',
                dict(tipo=tipo, locavel=locavel, responsaveis=responsaveis,
                    grupos=grupos, specific=specific, ret=ret, url_to_reserves=url_to_reserves))

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
                entries = ReservaEquipamento.objects.filter(data__year=year, data__month=month, data__day=day, locavel=espaco, estado="A")
            else:
                entries = ReservaEspacoFisico.objects.filter(data__year=year, data__month=month, data__day=day, locavel=espaco, estado="A")

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
    id_reservable = request.GET['id']
    data_numero = request.GET['data']
    try:
        horaInicio = request.GET['horaInicio']
        horaFim = request.GET['horaFim']
    except:
        horaInicio = None
        horaFim = None
    request.session['id_reservable'] = id_reservable
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

def filtroLocavelDisponivel(request, unit, tipo, sData, sHoraInicio, sHoraFim):
    data = datetime.strptime(sData, '%d%m%Y')
    horaInicio = datetime.strptime(sHoraInicio, '%H%M').time()
    horaFim = datetime.strptime(sHoraFim, '%H%M').time()
    atividade_dummy = Atividade.objects.create(nome='dummy', descricao='dummy')
    unit = Unidade.objects.get(id=unit)
    if tipo == 'f':
        query = unit.espacofisico_set.all()
        tipo_reserva = ReservaEspacoFisico

    elif tipo == 'e':
        query = unit.equipamento_set.all()
        tipo_reserva = ReservaEquipamento

    dummy_user = User.objects.create(username='dummy_user')
    for locavel in query:
        reserva_dummy = tipo_reserva.objects.create(data=data, horaInicio=horaInicio, horaFim=horaFim, atividade=atividade_dummy, usuario=dummy_user, ramal=1, finalidade='1', locavel=locavel)
        error = dict()
        reserva_dummy.verificaChoque(error)
        if bool(error) or (locavel.invisivel and not(request.user.is_superuser or request.user in locavel.responsavel.all())):
            query = query.exclude(id=locavel.id)
        reserva_dummy.delete()

    dummy_user.delete()
    atividade_dummy.delete()
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

def faq(request):
    faq_pages = list(FlatPage.objects.filter(url__contains='faq'))  # a list so it can be editted
    absolute_url = request.build_absolute_uri('/')
    # add 'pages' to urls to the template can use the true url
    return render(request, "agenda/faq.html", dict(pages=faq_pages))