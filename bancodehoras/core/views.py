from django.shortcuts import render, redirect
from django.views.generic.base import View
from core.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
from core.controller import FuncionalidadesCore
from movimentacao.controller import FormataDados, FuncionalidadesMovimentacao 
from movimentacao.views import seleciona_dados


# Colaborador
@login_required(login_url='login')
def dashboard(request):
    tamplate_name = 'core/dashboard/dashboard.html'
    setor = request.user.perfil.setor
    dados = seleciona_dados(request)
    dados['colaboradores_do_setor'] = setor.perfis_do_setor.all()
    dados['dados_grafico'] = formata_dados_do_grafico(request)
    return render(request, tamplate_name, dados)


def formata_dados_do_grafico(request):
    funcionalidade = FuncionalidadesMovimentacao([], [])
    autorizado = Status.objects.filter(autorizado=True)[0]
    perfis = request.user.perfil.setor.perfis_do_setor.all()
    resultado = []

    for perfil in perfis:
        bancos = perfil.movimentacoes.filter(entrada=True, status=autorizado)
        baixas = perfil.movimentacoes.filter(entrada=False, status=autorizado)
        resultado.append({
            'nome': perfil.nome,
            'total_horas': int(funcionalidade.total_de_horas_disponivel_do_perfil(autorizado, bancos, baixas).split(':')[0])
        })

    return resultado


# Administrador
@login_required(login_url='login')
def administrador(request):
    return redirect('administrador_setor')


@login_required(login_url='login')
def administrador_setor(request):
    tamplate_name = 'core/super/super-setor.html'
    dados = seleciona_dados(request)
    dados['setores'] = Setor.objects.all()
    dados['colaboradores'] = Perfil.objects.all()
    return render(request, tamplate_name, dados)


@login_required(login_url='login')
def administrador_mostra_setor(request, id):
    tamplate_name = 'core/super/mostra-setor.html'
    dados = seleciona_dados(request)
    dados['setor'] = Setor.objects.get(id=id)
    return render(request, tamplate_name, dados)


@login_required(login_url='login')
def administrador_mostra_usuario(request, id):
    tamplate_name = 'core/super/mostra-usuario.html'
    dados = seleciona_dados(request)
    dados['colaborador'] = User.objects.get(username=id)
    dados['setores'] = Setor.objects.all()
    return render(request, tamplate_name, dados)


@login_required(login_url='login')
def administrador_extra(request):
    tamplate_name = 'core/super/super-dados-extras.html'
    dados = seleciona_dados(request)
    dados['formasdepagamentos'] = FormaDePagamento.objects.all()
    dados['configuracoes'] = Hash.objects.all()
    return render(request, tamplate_name, dados)


# Setor
@login_required(login_url='login')
def setor(request):
    nome_setor = request.POST.get('nome_setor')
    Setor.objects.create(nome=nome_setor)
    messages.add_message(request, messages.INFO, 'Setor cadastrado com sucesso.')
    return redirect('administrador_setor')


@login_required(login_url='login')
def setor_atualiza(request, id):
    nome = request.POST.get('nome_setor')
    setor = Setor.objects.get(id=id)
    setor.nome = nome
    setor.save()
    return redirect('administrador_setor')


@login_required(login_url='login')
def setor_delete(request, id):
    setor = Setor.objects.get(id=id)
    colaboradores = setor.perfis_do_setor.all()

    if colaboradores.count() > 0:
        messages.add_message(request, messages.INFO, 'Impossível deletar, há colaboradores cadastrados no setor selecionado.')
    else:
        messages.add_message(request, messages.INFO, 'Setor deletado com sucesso.')
        setor.delete()

    return redirect('administrador_setor')


##
### Classes de controle
##
@login_required(login_url='login')
def status(request):
    if request.method == 'POST':
        nome_status = request.POST.get('nome_status')
        # analise = request.POST.get('padrao')
        # analise = False if analise is None else True
        status = request.POST.get('status')
        
        busca_status = Status.objects.filter(nome=nome_status)
        if len(busca_status) > 0:
            messages.add_message(request, messages.INFO, 'Status já cadastrado')
        else:
            analise = False
            autorizado = False
            if status == 'analise':
                salvar_novo_padrao_analise()
                analise = True
            elif status == 'autorizado':
                salvar_novo_padrao_autorizado()
                autorizado = True

            Status.objects.create(nome=nome_status, analise=analise, autorizado=autorizado)
            messages.add_message(request, messages.INFO, 'Status cadastrado com sucesso.')
            
    return redirect('administrador_extra')


@login_required(login_url='login')
def status_torna_padrao_analise(request, id):
    salvar_novo_padrao_analise(id)
    return redirect('administrador_extra')


@login_required(login_url='login')
def status_torna_padrao_autorizado(request, id):
    salvar_novo_padrao_autorizado(id)
    return redirect('administrador_extra')


@login_required(login_url='login')
def status_delete(request, id):
    status = Status.objects.get(id=id)
    if status.analise:
        if len(Status.objects.all()) != 1:
            status.delete()
            status = Status.objects.all()[0]
            status.analise = True
            status.save()
        else:
            status.delete()
    else:
        status.delete()
    return redirect('administrador_extra')


def salvar_novo_padrao_analise(id=None):
    if not id:
        status = Status.objects.all()
        for statu in status:
            statu.analise = False
            statu.save()
    else:
        status = Status.objects.all()
        for statu in status:
            if statu.id == id:
                statu.analise = True
                statu.save()
                continue

            statu.analise = False
            statu.save()


def salvar_novo_padrao_autorizado(id=None):
    if not id:
        status = Status.objects.all()
        for statu in status:
            statu.autorizado = False
            statu.save()
    else:
        status = Status.objects.all()
        for statu in status:
            if statu.id == id:
                statu.autorizado = True
                statu.save()
                continue

            statu.autorizado = False
            statu.save()


@login_required(login_url='login')
def forma_de_pagamento(request):
    forma_de_pagamento = request.POST.get('forma_de_pagamento')
    valor_duplo = request.POST.get('valor_duplo')
    valor_duplo = False if valor_duplo is None else True

    pagamentos = FormaDePagamento.objects.filter(nome=forma_de_pagamento)
    if len(pagamentos) > 0:
        messages.add_message(request, messages.INFO, 'Forma de pagamento já cadastrada.')
    else:
        FormaDePagamento.objects.create(nome=forma_de_pagamento, valor_duplo=valor_duplo)
        messages.add_message(request, messages.INFO, 'Forma de pagamento cadastrada com sucesso.')
    return redirect('administrador_extra')


@login_required(login_url='login')
def forma_de_pagamento_delete(request, id):
    pagamento = FormaDePagamento.objects.get(id=id)
    pagamento.delete()
    return redirect('administrador_extra')


@login_required(login_url='login')
def hash_edit(request, chave):
    pagamento = FormaDePagamento.objects.get(id=id)
    pagamento.delete()
    return redirect('administrador_extra')


@login_required(login_url='login')
def hash_edit(request, id):
    if request.method == 'POST':
        valor = request.POST.get('valor')
        if len(valor) > 0:
            funcionalidades = FuncionalidadesCore()
            hash_obj = Hash.objects.get(id=id)
            hash_obj.valor = valor
            hash_obj.save()
            
            messages.add_message(request, messages.INFO, 'Configuração modificada com sucesso.')
            return redirect('administrador_extra')
        messages.add_message(request, messages.INFO, 'Digite algo na configuração')
        return redirect('administrador_extra')
    else:
        dados = seleciona_dados(request)
        dados['configuracao'] = Hash.objects.get(id=id)
        return render(request, 'core/super/alterar-configuracao.html', dados)