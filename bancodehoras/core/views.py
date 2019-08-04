from django.shortcuts import render, redirect
from django.views.generic.base import View
from core.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
from core.controller import FormataDados, FuncionalidadesMovimentacao


class PainelDeControleSolicitacoesView(View):
    template_name = 'core/dashboard/dashboard-solicitacoes.html'

    def get(self, request):
        dados = {}
        dados['perfil_logado'] = request.user
        dados['solciitacoes_pendentes'] = self.seleciona_todas_movimentacoes(request.user.perfil.setor.perfis_do_setor.all())
        return render(request, self.template_name, dados)

    def seleciona_todas_movimentacoes(self, perfis):
        movimentacoes = []
        analise = Status.objects.all()[0]
        for perfil in perfis:
            movimentacoes.extend(
                perfil.movimentacoes.all().filter(
                    Q(finalizado=False),
                    Q(entrada=True)
                )
            )
        return movimentacoes


class PainelDeControleFolgasView(View):
    template_name = 'core/dashboard/dashboard-folgas.html'

    def get(self, request):
        dados = {}
        dados['perfil_logado'] = request.user
        dados['solciitacoes_pendentes'] = self.seleciona_todas_movimentacoes(request.user.perfil.setor.perfis_do_setor.all())
        return render(request, self.template_name, dados)

    def seleciona_todas_movimentacoes(self, perfis):
        movimentacoes = []
        analise = Status.objects.all()[0]
        for perfil in perfis:
            movimentacoes.extend(
                perfil.movimentacoes.all().filter(
                    Q(finalizado=False),
                    Q(entrada=False)
                )
            )
        return movimentacoes


class SolicitacaoBancoDeHorasView(View):
    template_name = 'core/usuario/usuario-bancodehoras.html'

    def get(self, request):
        dados = {}
        dados['perfil_logado'] = request.user
        dados['solicitacoes'] = request.user.perfil.movimentacoes.all().filter(entrada=True).order_by('data_cadastro')[::-1]
        return render(request, self.template_name, dados)

    def post(self, request):
        data_movimentacao = request.POST.get('data')
        hora_inicial = request.POST.get('hora_inicial')
        hora_final = request.POST.get('hora_final')
        motivo = request.POST.get('motivo')
        status = Status.objects.filter(analise=True)[0]
        solicitante = request.user.perfil
        format_data = FormataDados()
        hora_total = format_data.calcular_hora(hora_inicial, hora_final)
        data_movimentacao_formatada = datetime.strptime(data_movimentacao, '%Y-%m-%d').date()

        movimentacao = Movimentacao(
            data_movimentacao=data_movimentacao_formatada,
            hora_inicial = hora_inicial,
            hora_final = hora_final,
            hora_total = hora_total,
            motivo = motivo,
            status = status,
            entrada = True,
            colaborador = solicitante
        )
        movimentacao.save()

        log = 'Solicitação realizada com sucesso, solicitação de número: {}'.format(movimentacao.id)

        LogMovimentacao.objects.create(
            log=log,
            perfil_emissor=solicitante,
            movimentacao=movimentacao
        )

        messages.add_message(request, messages.INFO, 'Banco de horas solicitado com sucesso.')
        return redirect('solicitacoes')


class SolicitacaoBaixaView(View):
    template_name = 'core/usuario/usuario-folga.html'

    def get(self, request):
        dados = {}
        dados['perfil_logado'] = request.user
        dados['solicitacoes'] = request.user.perfil.movimentacoes.all().filter(entrada=False).order_by('data_cadastro')[::-1]
        return render(request, self.template_name, dados)

    def post(self, request):
        data_folga = request.POST.get('data_folga')
        total_horas = request.POST.get('horas_total')
        status = Status.objects.filter(analise=True)[0]
        solicitante = request.user.perfil
        total_horas = '0{}:00'.format(total_horas) if int(total_horas) < 10 else '{}:00'.format(total_horas)

        Movimentacao.objects.create(
            data_movimentacao=data_folga,
            entrada=False,
            hora_total=total_horas,
            status = status,
            colaborador = solicitante
        )

        messages.add_message(request, messages.INFO, 'Baixa solicitada com sucesso.')
        return redirect('solicitacoes')


##
### Administrador
##
@login_required(login_url='login')
def EscolhaDashboardView(request):
    tamplate_name = 'core/dashboard/opcaodeacesso.html'
    dados = {}
    dados['perfil_logado'] = request.user
    return render(request, tamplate_name, dados)    


# Colaborador
@login_required(login_url='login')
def DashboardView(request):
    tamplate_name = 'core/dashboard/dashboard.html'
    dados = {}
    setor = request.user.perfil.setor
    dados['perfil_logado'] = request.user
    dados['colaboradores_do_setor'] = setor.perfis_do_setor.all()
    return render(request, tamplate_name, dados)


# Administrador
@login_required(login_url='login')
def AdministradorView(request):
    return redirect('administrador_setor')


@login_required(login_url='login')
def AdministradorSetorView(request):
    tamplate_name = 'core/super/super-setor.html'
    dados = {}
    dados['setores'] = Setor.objects.all()
    dados['colaboradores'] = Perfil.objects.all()
    dados['perfil_logado'] = request.user
    return render(request, tamplate_name, dados)


@login_required(login_url='login')
def AdministradorMostraSetorView(request, id):
    tamplate_name = 'core/super/mostra-setor.html'
    dados = {}
    dados['setor'] = Setor.objects.get(id=id)
    dados['perfil_logado'] = request.user
    return render(request, tamplate_name, dados)


@login_required(login_url='login')
def AdministradorMostraUsuarioView(request, id):
    tamplate_name = 'core/super/mostra-usuario.html'
    dados = {}
    dados['colaborador'] = User.objects.get(username=id)
    dados['setores'] = Setor.objects.all()
    dados['perfil_logado'] = request.user
    return render(request, tamplate_name, dados)


@login_required(login_url='login')
def AdministradorExtraView(request):
    tamplate_name = 'core/super/super-dados-extras.html'
    dados = {}
    dados['perfil_logado'] = request.user
    dados['formasdepagamentos'] = FormaDePagamento.objects.all()
    dados['status'] = Status.objects.all()
    return render(request, tamplate_name, dados)


###
#### Solicitações do colaborador
###
@login_required(login_url='login')
def SolicitacaoView(request):
    dados = {}
    template_name = 'core/usuario/solicitacao.html'
    analise = Status.objects.filter(analise=True)[0]
    autorizado = Status.objects.filter(autorizado=True)[0]
    
    dados['perfil_logado'] = request.user
    dados['bancospendentes'] = request.user.perfil.movimentacoes.all().filter(
        Q(finalizado=False),
        Q(entrada=True),
        Q(status=analise)
    )
    dados['baixaspendentes'] = request.user.perfil.movimentacoes.all().filter(
        Q(finalizado=False),
        Q(entrada=False),
        Q(status=analise)
    )
    bancos = request.user.perfil.movimentacoes.all().filter(
        Q(finalizado=True),
        Q(entrada=True),
        Q(status=autorizado)
    )
    baixas = request.user.perfil.movimentacoes.all().filter(
        Q(finalizado=True),
        Q(entrada=False),
        Q(status=autorizado)
    )
    todos_os_bancos = Movimentacao.objects.filter(entrada=True, status=autorizado)
    todos_as_baixas = Movimentacao.objects.filter(entrada=False, status=autorizado)
    
    format_data = FuncionalidadesMovimentacao(todos_os_bancos, todos_as_baixas)
    dados['horas_disponiveis'] = format_data.total_de_horas_disponivel(autorizado)

    dados['horas_solicitadas'] = format_data.calcular_total_de_horas(dados['bancospendentes'])
    dados['baixas_solicitadas'] = format_data.calcular_total_de_horas(dados['baixaspendentes'])
    dados['horas_autorizadas'] = format_data.calcular_total_de_horas(bancos)
    dados['baixas_autorizadas'] = format_data.calcular_total_de_horas(baixas)
    return render(request, template_name, dados)


@login_required(login_url='login')
def listar_solicitacoes(request, id):
    tamplate_name = 'core/usuario/listagem-solicitacoes.html'
    dados = {}
    dados['perfil_logado'] = request.user
    dados['solicitacoes'] = User.objects.get(username=id).perfil.movimentacoes.all()

    return render(request, tamplate_name, dados)


@login_required(login_url='login')
def SolicitacaoMostrarView(request, id):
    template_name = 'core/dashboard/dashboard-mostra-solicitacao.html'

    if request.method == 'POST':
        id_status = int(request.POST.get('id_status'))
        id_movimentacao = int(request.POST.get('id_movimentacao'))
        descricao = request.POST.get('descricao')

        forma_de_pagamento = None
        if request.POST.get('id_pagamento'):
            id_pagamento = int(request.POST.get('id_pagamento'))
            forma_de_pagamento = FormaDePagamento.objects.get(id=id_pagamento)
        
        status = Status.objects.get(id=id_status)
        movimentacao = Movimentacao.objects.get(id=id_movimentacao)
        perfil = request.user.perfil

        if status.autorizado:
            movimentacao.finalizado = True
        else:
            movimentacao.finalizado = False

        msg_padrao = '{}'.format(descricao)
        movimentacao.status = status
        movimentacao.forma_de_pagamento = forma_de_pagamento
        movimentacao.save()

        LogMovimentacao.objects.create(log=msg_padrao, perfil_emissor=perfil, movimentacao=movimentacao)

    dados = {}
    dados['perfil_logado'] = request.user
    dados['solicitacao'] = Movimentacao.objects.get(id=id)
    dados['status'] = Status.objects.all()
    dados['forma_de_pagamento'] = FormaDePagamento.objects.all()

    return render(request, template_name, dados)


@login_required(login_url='login')
def SolicitacaoFinalizarView(request, id):
    movimentacao = Movimentacao.objects.get(id=id)
    analise = Status.objects.filter(analise=True)[0]

    if movimentacao.status == analise:
        messages.add_message(request, messages.INFO, 'Impossível finalizar uma movimentação em análise, por favor verifique o status antes de finalizar.')
    else:
        movimentacao.finalizado = True
        movimentacao.save()
        perfil = request.user.perfil
        msg_padrao = 'Solicitação finalizada'
        LogMovimentacao.objects.create(log=msg_padrao, perfil_emissor=perfil, movimentacao=movimentacao)

    return redirect('solicitacoes_mostrar', id=id)


# Setor
@login_required(login_url='login')
def SetorView(request):
    nome_setor = request.POST.get('nome_setor')
    Setor.objects.create(nome=nome_setor)
    messages.add_message(request, messages.INFO, 'Setor cadastrado com sucesso.')
    return redirect('administrador_setor')


@login_required(login_url='login')
def SetorAtualizaView(request, id):
    nome = request.POST.get('nome_setor')
    setor = Setor.objects.get(id=id)
    setor.nome = nome
    setor.save()
    return redirect('administrador_setor')


@login_required(login_url='login')
def SetorDeleteView(request, id):
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
def StatusView(request):
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
def StatusTornaPadraoAnaliseView(request, id):
    salvar_novo_padrao_analise(id)
    return redirect('administrador_extra')


@login_required(login_url='login')
def StatusTornaPadraoAutorizadoView(request, id):
    salvar_novo_padrao_autorizado(id)
    return redirect('administrador_extra')


@login_required(login_url='login')
def StatusDeleteView(request, id):
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
def FormaDePagamentoView(request):
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
def FormaDePagamentoDeletarView(request, id):
    pagamento = FormaDePagamento.objects.get(id=id)
    pagamento.delete()
    return redirect('administrador_extra')
