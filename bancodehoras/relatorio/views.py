# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from relatorio import controller
from datetime import datetime
from core.models import *
from movimentacao.views import seleciona_dados
import os

# Create your views here.
@login_required(login_url='login')
def relatorio(request):
    if request.method == 'POST':
        data_inicial = request.POST.get('data_inicial')
        data_final = request.POST.get('data_final')
        status = request.POST.get('status')
        andamento = request.POST.get('andamento')
        colaborador = request.POST.get('colaborador')
        forma_pagamento = request.POST.get('forma_pagamento')
        tipo_movimentacao = request.POST.get('tipo_movimentacao')

        inicio = datetime.strptime(data_inicial, '%Y-%m-%d')
        fim = datetime.strptime(data_final, '%Y-%m-%d')
        dados = Movimentacao.objects.filter(data_movimentacao__range=(inicio, fim))

        if status != '0' and status != '': # Status
            print('=========================================')
            print('Aplicou o filtro de Status')
            print('=========================================')
            id_aux = int(status)
            status = Status.objects.get(id=id_aux)
            dados = dados.filter(status=status)

        if andamento != '0' and andamento != '': # Andamento da solicitação
            print('=========================================')
            print('Aplicou o filtro de Andamento da solicitação')
            print('=========================================')
            id_aux = False
            if id_aux == '1':
                id_aux = True
            dados = dados.filter(finalizado=id_aux)

        if colaborador != '0' and colaborador != '': # colaborador especifico
            print('=========================================')
            print('Aplicou o filtro de Colaborador especifico')
            print('=========================================')
            id_aux = int(colaborador)
            colaborador = Perfil.objects.get(id=id_aux)
            dados = dados.filter(colaborador=colaborador)

        if forma_pagamento != '0' and forma_pagamento != '': # Forma de pagamento
            print('=========================================')
            print('Aplicou o filtro de Forma de pagamento')
            print('=========================================')
            id_aux = int(forma_pagamento)
            forma_pagamento = Status.objects.get(id=id_aux)
            dados = dados.filter(forma_de_pagamento=forma_pagamento)

        if tipo_movimentacao != '0' and tipo_movimentacao != '': # Tipo de movimentacao
            print('=========================================')
            print('Aplicou o filtro de tipo de movimentacao')
            print('=========================================')
            id_aux = False
            if tipo_movimentacao == '1':
                id_aux = True
            dados = dados.filter(entrada=id_aux)

        import pdb; pdb.set_trace()

    dados = seleciona_dados(request)
    return render(request, 'relatorio/relatorio.html', dados)


def formata_dados_do_relatorio(dados, todas_as_movimentacoes=False, tipo_movimentacao=None):
    pass
    

def gera_teste(request):
    pasta = 'relatorio/arquivos/'
    nome_arquivo = 'teste_teste.xls'
    arquivo = '{}{}'.format(pasta, nome_arquivo)
    filepath = os.path.join(settings.MEDIA_ROOT, arquivo)

    dados = {'titulos': [], 'linhas': []}
    info = Movimentacao.objects.all()
    dados['titulos'] = ['Data cadastro', 'motivo', 'colaborador']
    add = []
    for i in info:
        add.append([i.data_cadastro, i.motivo, i.colaborador.nome])
    dados['linhas'] = add
    controller.gera_relatorio(dados, 'teste_teste')
    
    if os.path.exists(filepath):
        with open(filepath, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filepath)
            return response
            
    return HttpResponse('Arquivo não encontrado.')
    


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