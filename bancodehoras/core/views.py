from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.controller import FuncionalidadesCore
from core.models import *
from movimentacao.controller import FuncionalidadesMovimentacao
from movimentacao.views import seleciona_dados
from core import constants


def isntalar_sistema(request):
    func = FuncionalidadesCore()
    if func.superuser(request):
        if len(Hash.objects.all()) == 0:
            print('Instalando sistema, criando chave valor')
            nome = 'Valor das horas'
            chave = constants.VALOR_HORA
            valor = 1
            Hash.objects.create(nome=nome, chave=chave, valor=valor)

        if len(FormaDePagamento.objects.all()) == 0:
            print('Instalando sistema, criando forma de pagamento')
            FormaDePagamento.objects.create(nome='Dinheiro')

        if len(Status.objects.all()) == 0:
            print('Instalando sistema, criando status')
            Status.objects.create(nome='Análise', analise=True)
            Status.objects.create(nome='Autorizado', autorizado=True)
            Status.objects.create(nome='Cancelado')

        print('Sistema instalado')
    else:
        print('Usuario sem permissao para instalar o sistema')
    return redirect('logout')


# Colaborador
@login_required(login_url='login')
def dashboard(request):
    func = FuncionalidadesCore()
    if not func.administardor(request):
        return redirect('solicitacoes')
    
    tamplate_name = 'core/dashboard/dashboard.html'
    setor = request.user.perfil.setor
    dados = seleciona_dados(request)
    dados['colaboradores_do_setor'] = setor.perfis_do_setor.all()
    dados['dados_grafico'] = formata_dados_do_grafico(request)
    return render(request, tamplate_name, dados)


def formata_dados_do_grafico(request):
    try:
        funcionalidade = FuncionalidadesMovimentacao([], [])
        autorizado = Status.objects.filter(autorizado=True)[0]
        perfis = request.user.perfil.setor.perfis_do_setor.all()
        resultado = []

        for perfil in perfis:
            bancos = perfil.movimentacoes.filter(entrada=True, status=autorizado)
            baixas = perfil.movimentacoes.filter(entrada=False, status=autorizado)
            resultado.append({
                'nome': perfil.nome,
                'total_horas': int(
                    funcionalidade.total_de_horas_disponivel_do_perfil(autorizado, bancos, baixas).split(':')[0])
            })

        return resultado

    except Exception:
        return []


# Administrador
@login_required(login_url='login')
def administrador(request):
    func = FuncionalidadesCore()
    if not func.superuser(request):
        return redirect('solicitacoes')
    return redirect('setor')


@login_required(login_url='login')
def administrador_mostra_setor(request, id):
    func = FuncionalidadesCore()
    if not func.superuser(request):
        return redirect('solicitacoes')

    tamplate_name = 'core/super/mostra-setor.html'
    dados = seleciona_dados(request)
    dados['setor'] = Setor.objects.get(id=id)
    return render(request, tamplate_name, dados)


@login_required(login_url='login')
def administrador_extra(request):
    func = FuncionalidadesCore()
    if not func.superuser(request):
        return redirect('solicitacoes')
    
    tamplate_name = 'core/super/super-dados-extras.html'
    dados = seleciona_dados(request)
    dados['formasdepagamentos'] = FormaDePagamento.objects.all()
    dados['configuracoes'] = Hash.objects.all()
    return render(request, tamplate_name, dados)


# Setor
@login_required(login_url='login')
def setor(request):
    func = FuncionalidadesCore()
    if not func.superuser(request):
        return redirect('solicitacoes')

    if request.method == 'POST':
        try:
            nome_setor = request.POST.get('nome_setor')
            if len(nome_setor) == 0:
                messages.add_message(request, messages.INFO, 'Erro no cadastro, nome inválido.')
            elif len(Setor.objects.filter(nome=nome_setor)) > 0:
                messages.add_message(request, messages.INFO, 'Erro no cadastro, setor já cadastrado.')
            else:
                Setor.objects.create(nome=nome_setor)
                messages.add_message(request, messages.INFO, 'Setor cadastrado com sucesso.')
            return redirect('setor')            
        except Exception:
            messages.add_message(request, messages.INFO, 'Erro no cadastro do setor, contate o administrador do sistema.')
            return redirect('setor')
    else:
        dados = seleciona_dados(request)
        dados['setores'] = Setor.objects.all()
        dados['colaboradores'] = Perfil.objects.all()
        return render(request, 'core/super/super-setor.html', dados)


@login_required(login_url='login')
def setor_atualiza(request, id):
    func = FuncionalidadesCore()
    if not func.superuser(request):
        return redirect('solicitacoes')

    if request.method == 'POST':
        try:
            nome_setor = request.POST.get('nome_setor')
            if len(nome_setor) == 0:
                messages.add_message(request, messages.INFO, 'Erro na atualização, nome inválido.')
            elif len(Setor.objects.filter(nome=nome_setor)) > 0:
                messages.add_message(request, messages.INFO, 'Erro na atualização, setor já cadastrado.')
            else:
                setor = Setor.objects.get(id=id)
                setor.nome = nome_setor
                setor.save()
            return redirect('setor')
        except Exception:
            return redirect('setor')
    return redirect('setor')


@login_required(login_url='login')
def setor_delete(request, id):
    func = FuncionalidadesCore()
    if not func.superuser(request):
        return redirect('solicitacoes')

    setor = Setor.objects.get(id=id)
    colaboradores = setor.perfis_do_setor.all()

    if colaboradores.count() > 0:
        messages.add_message(request, messages.INFO, 'Impossível deletar, há colaboradores cadastrados no setor '
                                                     'selecionado.')
    else:
        messages.add_message(request, messages.INFO, 'Setor deletado com sucesso.')
        setor.delete()

    return redirect('setor')


##
### Classes de controle
##
@login_required(login_url='login')
def status(request):
    func = FuncionalidadesCore()
    if not func.superuser(request):
        return redirect('solicitacoes')

    if request.method == 'POST':
        try:
            nome_status = request.POST.get('nome_status')
            status = request.POST.get('status')
            
            if len(nome_status) == 0 or len(status) == 0:
                messages.add_message(request, messages.INFO, 'Erro no cadastro, dados inválidos para cadastro')
            elif len(Status.objects.filter(nome=nome_status)) > 0:
                messages.add_message(request, messages.INFO, 'Erro no cadastro, status já cadastrado')
            else:
                analise = False
                autorizado = False
                if status == 'analise':
                    salvar_novo_padrao_analise(request)
                    analise = True
                elif status == 'autorizado':
                    salvar_novo_padrao_autorizado(request)
                    autorizado = True
                Status.objects.create(nome=nome_status, analise=analise, autorizado=autorizado)
                messages.add_message(request, messages.INFO, 'Status cadastrado com sucesso.')
        except Exception:
            messages.add_message(request, messages.INFO, 'Erro no cadastro, verifique se todos os campos estão preenchidos corretamente.')
            return redirect('administrador_extra')
    return redirect('administrador_extra')


@login_required(login_url='login')
def status_torna_padrao_analise(request, id):
    func = FuncionalidadesCore()
    if not func.superuser(request):
        return redirect('solicitacoes')

    salvar_novo_padrao_analise(request, id)
    return redirect('administrador_extra')


@login_required(login_url='login')
def status_torna_padrao_autorizado(request, id):
    func = FuncionalidadesCore()
    if not func.superuser(request):
        return redirect('solicitacoes')

    salvar_novo_padrao_autorizado(request, id)
    return redirect('administrador_extra')


@login_required(login_url='login')
def status_delete(request, id):
    func = FuncionalidadesCore()
    if not func.superuser(request):
        return redirect('solicitacoes')

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


@login_required(login_url='login')
def status_editar(request, id):
    func = FuncionalidadesCore()
    if not func.superuser(request):
        return redirect('solicitacoes')
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        if len(nome) > 0:
            status = Status.objects.get(id=id)
            status.nome = nome
            status.save()
            messages.add_message(request, messages.INFO, 'Status modificado com sucesso.')
        else:
            messages.add_message(request, messages.INFO, 'Digite algo para editar')
        return redirect('administrador_extra')
    else:
        dados = seleciona_dados(request)
        dados['status'] = Status.objects.get(id=id)
        return render(request, 'core/super/alterar-status.html', dados)


def salvar_novo_padrao_analise(request, id=None):
    if not id:
        status = Status.objects.all()
        for statu in status:
            statu.analise = False
            statu.save()
    else:
        alterar_demais = True
        status_aux = Status.objects.get(id=id)

        if not status_aux.autorizado:
            status_aux.analise = True
            status_aux.save()
        else:
            alterar_demais = False
            messages.add_message(request, messages.INFO, 'Impossível um status ser do tipo análise e autorizado ao mesmo tempo.')

        if alterar_demais:
            for status in Status.objects.all():
                if status.id == id:
                    continue
                status.analise = False
                status.save()



def salvar_novo_padrao_autorizado(request, id=None):
    if not id:
        status = Status.objects.all()
        for statu in status:
            statu.autorizado = False
            statu.save()
    else:
        alterar_demais = True
        status_aux = Status.objects.get(id=id)

        if not status_aux.analise:
            status_aux.autorizado = True
            status_aux.save()
        else:
            alterar_demais = False
            messages.add_message(request, messages.INFO, 'Impossível um status ser do tipo análise e autorizado ao mesmo tempo.')

        if alterar_demais:
            for status in Status.objects.all():
                if status.id == id:
                    continue
                status.autorizado = False
                status.save()


@login_required(login_url='login')
def forma_de_pagamento(request):
    func = FuncionalidadesCore()
    if not func.superuser(request):
        return redirect('solicitacoes')

    if request.method == 'POST':
        forma_de_pagamento = request.POST.get('forma_de_pagamento')
        pagamentos = FormaDePagamento.objects.filter(nome=forma_de_pagamento)
        if len(pagamentos) > 0:
            messages.add_message(request, messages.INFO, 'Forma de pagamento já cadastrada.')
        else:
            FormaDePagamento.objects.create(nome=forma_de_pagamento)
            messages.add_message(request, messages.INFO, 'Forma de pagamento cadastrada com sucesso.')
    return redirect('administrador_extra')


@login_required(login_url='login')
def forma_de_pagamento_delete(request, id):
    func = FuncionalidadesCore()
    if not func.superuser(request):
        return redirect('solicitacoes')

    pagamento = FormaDePagamento.objects.get(id=id)
    pagamento.delete()
    return redirect('administrador_extra')


@login_required(login_url='login')
def forma_de_pagamento_editar(request, id):
    func = FuncionalidadesCore()
    if not func.superuser(request):
        return redirect('solicitacoes')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        if len(nome) > 0:
            pagamento = FormaDePagamento.objects.get(id=id)
            pagamento.nome = nome
            pagamento.save()
            messages.add_message(request, messages.INFO, 'Forma de pagamento modificado com sucesso.')
        else:
            messages.add_message(request, messages.INFO, 'Digite algo para editar')
        return redirect('administrador_extra')
    else:
        dados = seleciona_dados(request)
        dados['pagamento'] = FormaDePagamento.objects.get(id=id)
        return render(request, 'core/super/alterar-formadepagamento.html', dados)


@login_required(login_url='login')
def hash_edit(request, id):
    func = FuncionalidadesCore()
    if not func.superuser(request):
        return redirect('solicitacoes')
    
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
