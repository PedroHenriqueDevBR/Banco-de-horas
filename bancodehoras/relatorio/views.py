# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from relatorio import controller
from core.models import *
from movimentacao.views import seleciona_dados
import os

# Create your views here.
@login_required(login_url='login')
def relatorio(request):
    dados = seleciona_dados(request)
    return render(request, 'relatorio/relatorio.html', dados)


@login_required(login_url='login')
def relarorio_de_perfis(request):
    perfis = Perfil.objects.all()
    controller.relatorio_de_usuarios_por_setor(perfis)
    return redirect('dashboard')


@login_required(login_url='login')
def relarorio_de_perfis_baixa(request, arquivo):
    pasta = 'relatorio/arquivos/'
    nome_arquivo = arquivo
    arquivo = '{}{}'.format(pasta, nome_arquivo)
    filepath = os.path.join(settings.MEDIA_ROOT, arquivo)
        
    if os.path.exists(filepath):
        with open(filepath, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filepath)
            return response
            
    return HttpResponse('Arquivo não encontrado.')


@login_required(login_url='login')
def solicitacoes_pendentes_do_perfil(request, id):
    try:
        perfil = Perfil.objects.get(id=id)
        controller.relatorio_solicitacoes_pendentes_do_perfil(perfil)

        pasta = 'relatorio/arquivos/'
        nome_arquivo = 'solicitacoes.xls'
        arquivo = '{}{}'.format(pasta, nome_arquivo)
        filepath = os.path.join(settings.MEDIA_ROOT, arquivo)
        
        if os.path.exists(filepath):
            with open(filepath, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filepath)
                return response
        else:
            return HttpResponse('Arquivo não encontrado.')

    except Exception:
        messages.add_message(request, messages.INFO, 'Usuário não localizado')
        return redirect('dashboard')


@login_required(login_url='login')
def solicitacoes_pendentes_do_meu_setor(request):
    try:
        user = request.user
        usuarios_do_setor = user.perfil.setor.perfis_do_setor.all()
        controller.relatorio_solicitacoes_do_meu_setor(usuarios_do_setor)

        pasta = 'relatorio/arquivos/'
        nome_arquivo = 'solicitacoes_pendentes.xls'
        arquivo = '{}{}'.format(pasta, nome_arquivo)
        filepath = os.path.join(settings.MEDIA_ROOT, arquivo)
        
        if os.path.exists(filepath):
            with open(filepath, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filepath)
                return response
        else:
            return HttpResponse('Arquivo não encontrado.')

    except Exception:
        messages.add_message(request, messages.INFO, 'Usuário não localizado')
        return redirect('dashboard')

    return redirect('dashboard')