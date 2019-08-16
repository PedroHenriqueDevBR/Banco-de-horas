from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
from movimentacao.controller import FormataDados, FuncionalidadesMovimentacao, Utilidades
from core.controller import FuncionalidadesCore
from core.models import *
from django.core.paginator import Paginator


class PainelDeControleSolicitacoesView(View):
    template_name = 'core/dashboard/dashboard-solicitacoes.html'

    def get(self, request):
        func = Utilidades()
        dados = seleciona_dados(request)
        setor = request.user.perfil.setor
        dados['colaboradores_do_setor'] = setor.perfis_do_setor.all()
        dados['dados_grafico'] = self.formata_dados_do_grafico(request)

        # Sistema de paginação
        paginacao = Paginator(func.seleciona_todas_movimentacoes(perfis=request.user.perfil.setor.perfis_do_setor.all(), entrada=True), 5)
        page = request.GET.get('pagina')
        dados['username'] = id

        try:
            dados['solciitacoes_pendentes'] = paginacao.get_page(page)
        except Exception:
            dados['solciitacoes_pendentes'] = paginacao.page(1)
            if page is not None:
                messages.add_message(request, messages.INFO, 'A página {} não existe'.format(page))

        return render(request, self.template_name, dados)

    def formata_dados_do_grafico(self, request):
        funcionalidade = FuncionalidadesMovimentacao([], [])
        autorizado = Status.objects.filter(autorizado=True)[0]
        perfis = request.user.perfil.setor.perfis_do_setor.all()
        resultado = []

        for perfil in perfis:
            bancos = perfil.movimentacoes.filter(
                entrada=True, status=autorizado)
            baixas = perfil.movimentacoes.filter(
                entrada=False, status=autorizado)
            resultado.append({
                'nome': perfil.nome,
                'total_horas': int(funcionalidade.total_de_horas_disponivel_do_perfil(autorizado, bancos, baixas).split(':')[0])
            })

        return resultado


class PainelDeControleFolgasView(View):
    template_name = 'core/dashboard/dashboard-folgas.html'

    def get(self, request):
        func = Utilidades()
        dados = seleciona_dados(request)
        setor = request.user.perfil.setor
        dados['colaboradores_do_setor'] = setor.perfis_do_setor.all()
        dados['dados_grafico'] = self.formata_dados_do_grafico(request)

        # Sistema de paginação
        paginacao = Paginator(func.seleciona_todas_movimentacoes(perfis=request.user.perfil.setor.perfis_do_setor.all(), entrada=False), 5)
        page = request.GET.get('pagina')
        dados['username'] = id

        try:
            dados['solciitacoes_pendentes'] = paginacao.get_page(page)
        except Exception:
            dados['solciitacoes_pendentes'] = paginacao.page(1)
            if page is not None:
                messages.add_message(request, messages.INFO, 'A página {} não existe'.format(page))

        return render(request, self.template_name, dados)

    def formata_dados_do_grafico(self, request):
        funcionalidade = FuncionalidadesMovimentacao([], [])
        autorizado = Status.objects.filter(autorizado=True)[0]
        perfis = request.user.perfil.setor.perfis_do_setor.all()
        resultado = []

        for perfil in perfis:
            bancos = perfil.movimentacoes.filter(
                entrada=True, status=autorizado)
            baixas = perfil.movimentacoes.filter(
                entrada=False, status=autorizado)
            resultado.append({
                'nome': perfil.nome,
                'total_horas': int(funcionalidade.total_de_horas_disponivel_do_perfil(autorizado, bancos, baixas).split(':')[0])
            })

        return resultado


class SolicitacaoBancoDeHorasView(View):
    template_name = 'movimentacao/usuario-bancodehoras.html'

    def get(self, request):
        dados = seleciona_dados(request)

        # Sistema de paginação
        paginacao = Paginator(request.user.perfil.movimentacoes.all().filter(entrada=True).order_by('data_cadastro')[::-1], 5)
        page = request.GET.get('pagina')

        try:
            dados['solicitacoes'] = paginacao.get_page(page)
        except Exception:
            dados['solicitacoes'] = paginacao.page(1)
            if page is not None:
                messages.add_message(request, messages.INFO, 'A página {} não existe'.format(page))

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
        data_movimentacao_formatada = datetime.strptime(
            data_movimentacao, '%Y-%m-%d').date()

        movimentacao = Movimentacao(
            data_movimentacao=data_movimentacao_formatada,
            hora_inicial=hora_inicial,
            hora_final=hora_final,
            hora_total=hora_total,
            motivo=motivo,
            status=status,
            entrada=True,
            colaborador=solicitante
        )
        movimentacao.save()

        log = 'Solicitação realizada com sucesso, solicitação de número: {}'.format(
            movimentacao.id)

        LogMovimentacao.objects.create(
            log=log,
            perfil_emissor=solicitante,
            movimentacao=movimentacao
        )

        messages.add_message(request, messages.INFO,
                             'Banco de horas solicitado com sucesso.')
        return redirect('solicitacoes')


class SolicitacaoBaixaView(View):
    template_name = 'movimentacao/usuario-folga.html'

    def get(self, request):
        dados = seleciona_dados(request)

        # Sistema de paginação
        paginacao = Paginator(request.user.perfil.movimentacoes.all().filter(entrada=False).order_by('data_cadastro')[::-1], 5)
        page = request.GET.get('pagina')

        try:
            dados['solicitacoes'] = paginacao.get_page(page)
        except Exception:
            dados['solicitacoes'] = paginacao.page(1)
            if page is not None:
                messages.add_message(request, messages.INFO, 'A página {} não existe'.format(page))
        return render(request, self.template_name, dados)

    def post(self, request):
        data_folga = request.POST.get('data_folga')
        total_horas = request.POST.get('horas_total')
        status = Status.objects.filter(analise=True)[0]
        solicitante = request.user.perfil
        total_horas = '0{}:00'.format(total_horas) if int(
            total_horas) < 10 else '{}:00'.format(total_horas)

        Movimentacao.objects.create(
            data_movimentacao=data_folga,
            entrada=False,
            hora_total=total_horas,
            status=status,
            colaborador=solicitante
        )

        messages.add_message(request, messages.INFO,
                             'Baixa solicitada com sucesso.')
        return redirect('solicitacoes')


###
# Solicitações do colaborador
###
@login_required(login_url='login')
def solicitacao(request):
    template_name = 'movimentacao/solicitacao.html'
    dados = seleciona_dados(request)
    return render(request, template_name, dados)


@login_required(login_url='login')
def listar_solicitacoes(request, id):
    tamplate_name = 'movimentacao/listagem-solicitacoes.html'
    dados = seleciona_dados(request)

    # Sistema de paginação
    paginacao = Paginator(User.objects.get(
        username=id).perfil.movimentacoes.all()[::-1], 15)
    page = request.GET.get('pagina')
    dados['username'] = id

    try:
        dados['solicitacoes'] = paginacao.get_page(page)
    except Exception:
        dados['solicitacoes'] = paginacao.page(1)
        if page is not None:
            messages.add_message(request, messages.INFO,
                                 'A página {} não existe'.format(page))

    return render(request, tamplate_name, dados)


@login_required(login_url='login')
def solicitacao_mostra_view(request, id):
    template_name = 'movimentacao/mostra-solicitacao.html'

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

        LogMovimentacao.objects.create(
            log=msg_padrao, perfil_emissor=perfil, movimentacao=movimentacao)

    dados = seleciona_dados(request)
    dados['solicitacao'] = Movimentacao.objects.get(id=id)
    return render(request, template_name, dados)


@login_required(login_url='login')
def solciitacao_finaliza(request, id):
    movimentacao = Movimentacao.objects.get(id=id)
    analise = Status.objects.filter(analise=True)[0]

    if movimentacao.status == analise:
        messages.add_message(
            request, messages.INFO, 'Impossível finalizar uma movimentação em análise, por favor verifique o status antes de finalizar.')
    else:
        movimentacao.finalizado = True
        movimentacao.save()
        perfil = request.user.perfil
        msg_padrao = 'Solicitação finalizada'
        LogMovimentacao.objects.create(
            log=msg_padrao, perfil_emissor=perfil, movimentacao=movimentacao)

    return redirect('solicitacoes_mostrar', id=id)


def seleciona_dados(request):
    dados = {}

    try:
        analise = Status.objects.filter(analise=True)[0]
    except Exception:
        analise = None
    try:
        autorizado = Status.objects.filter(autorizado=True)[0]
    except Exception:
        autorizado = None

    bancos = request.user.perfil.movimentacoes.all().filter(
        Q(finalizado=True), Q(entrada=True), Q(status=autorizado))
    baixas = request.user.perfil.movimentacoes.all().filter(
        Q(finalizado=True), Q(entrada=False), Q(status=autorizado))
    todos_os_bancos = Movimentacao.objects.filter(
        entrada=True, status=autorizado)
    todos_as_baixas = Movimentacao.objects.filter(
        entrada=False, status=autorizado)
    meus_bancos = request.user.perfil.movimentacoes.filter(
        entrada=True, status=autorizado)
    minhas_baixas = request.user.perfil.movimentacoes.filter(
        entrada=False, status=autorizado)

    format_data = FuncionalidadesMovimentacao(todos_os_bancos, todos_as_baixas)
    my_format = FuncionalidadesMovimentacao(meus_bancos, minhas_baixas)
    func = Utilidades()

    dados['bancospendentes'] = request.user.perfil.movimentacoes.all().filter(
        Q(entrada=True), Q(status=analise))
    dados['baixaspendentes'] = request.user.perfil.movimentacoes.all().filter(
        Q(entrada=False), Q(status=analise))
    dados['totalpendente'] = len(
        dados['bancospendentes']) + len(dados['baixaspendentes'])
    dados['horas_disponiveis'] = my_format.total_de_horas_disponivel(
        autorizado)
    dados['perfil_logado'] = request.user
    dados['horas_solicitadas'] = format_data.calcular_total_de_horas(
        dados['bancospendentes'])
    dados['baixas_solicitadas'] = format_data.calcular_total_de_horas(
        dados['baixaspendentes'])
    dados['horas_autorizadas'] = format_data.calcular_total_de_horas(bancos)
    dados['baixas_autorizadas'] = format_data.calcular_total_de_horas(baixas)
    dados['status'] = Status.objects.all()
    dados['forma_de_pagamento'] = FormaDePagamento.objects.all()

    return dados
