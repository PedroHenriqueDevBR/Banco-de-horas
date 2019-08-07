# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from relatorio import controller
from core.models import *
import os

# Create your views here.
@login_required(login_url='login')
def relarorio_de_perfis(request):
    perfis = Perfil.objects.all()
    controller.relatorio_de_usuarios_por_setor(perfis)
    return redirect('dashboard')


@login_required(login_url='login')
def relarorio_de_perfis_baixa(request, arquivo):
    pasta = 'relatorio/arquivos/'
    nome_arquivo = 'relatorio.xls'

    filepath = '{}{}'.format(pasta, nome_arquivo)
    file = pasta + nome_arquivo
    path = os.path.join(file).decode("utf8")
    data = open(path, encoding = "utf-8")


    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="relatorio.xls"'
    response.write(data)
    return response
