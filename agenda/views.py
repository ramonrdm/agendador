# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from django.http import HttpResponse

# Create your views here.
def index(request):

	titulo = "Agendador de espaço físico do CCS"
	corpo = "Bem vindo ao Agendador de espaço físico do CCS"
	return render_to_response("index.html",{'corpo':corpo,"titulo":titulo})

def requisitos(request):
	titulo = "Requisitos do Agendador CCS"
	return render_to_response("requisitos.html", {'titulo':titulo})