from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import OperationalError
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.models import User

import apps.core.constants as constant
from apps.core.models import Hash
from apps.movimentacao.models import (
    FormaPagamento,
    LogSolicitacaoHoras,
    Movimentacao,
    SolicitacaoHoras,
    SolicitacaoPagamento,
)
from apps.core.views.controller import FuncionalidadesCore
from apps.movimentacao.controller import (
    FormataDados,
    FuncionalidadesMovimentacao,
    Utilidades,
)


class PainelDeControleSolicitacoesView(View):
    template_name = "core/dashboard/dashboard-solicitacoes.html"

    def get(self, request):
        func = FuncionalidadesCore()
        if not func.administardor(request):
            return redirect("solicitacoes")

        func = Utilidades()
        dados = seleciona_dados(request)
        setor = request.user.perfil.setor
        dados["colaboradores_do_setor"] = setor.internos.all()
        dados["dados_grafico"] = self.formata_dados_do_grafico(request)

        # Sistema de paginação
        paginacao = Paginator(
            func.seleciona_todas_movimentacoes(
                perfis=request.user.perfil.setor.internos.all(), entrada=True
            ),
            5,
        )
        page = request.GET.get("pagina")
        dados["username"] = id

        try:
            dados["solicitacoes_pendentes"] = paginacao.get_page(page)
        except Exception:
            dados["solicitacoes_pendentes"] = paginacao.page(1)
            if page is not None:
                messages.add_message(
                    request, messages.INFO, "A página {} não existe".format(page)
                )

        return render(request, self.template_name, dados)

    def formata_dados_do_grafico(self, request):
        try:
            funcionalidade = FuncionalidadesMovimentacao([], [])
            perfis = request.user.perfil.setor.internos.all()
            resultado = []

            for perfil in perfis:
                bancos = perfil.solicitacoes_horas.filter(
                    status=Movimentacao.DEFERIDO,
                )
                baixas = perfil.solicitacoes_pagamentos.filter(
                    status=Movimentacao.DEFERIDO,
                )
                resultado.append(
                    {
                        "nome": perfil.nome,
                        "total_horas": int(
                            funcionalidade.total_de_horas_disponivel_do_perfil(
                                Movimentacao.DEFERIDO,
                                bancos,
                                baixas,
                            ).split(":")[0]
                        ),
                    }
                )

            return resultado
        except Exception:
            return []


class PainelDeControleFolgasView(View):
    template_name = "core/dashboard/dashboard-folgas.html"

    def get(self, request):
        func = FuncionalidadesCore()
        if not func.administardor(request):
            return redirect("solicitacoes")

        func = Utilidades()
        dados = seleciona_dados(request)
        setor = request.user.perfil.setor
        dados["colaboradores_do_setor"] = setor.internos.all()
        dados["dados_grafico"] = self.formata_dados_do_grafico(request)

        # Sistema de paginação
        paginacao = Paginator(
            func.seleciona_todas_movimentacoes(
                perfis=request.user.perfil.setor.internos.all(), entrada=False
            ),
            5,
        )
        page = request.GET.get("pagina")
        dados["username"] = id

        try:
            dados["solicitacoes_pendentes"] = paginacao.get_page(page)
        except Exception:
            dados["solicitacoes_pendentes"] = paginacao.page(1)
            if page is not None:
                messages.add_message(
                    request, messages.INFO, "A página {} não existe".format(page)
                )

        return render(request, self.template_name, dados)

    def formata_dados_do_grafico(self, request):
        try:
            funcionalidade = FuncionalidadesMovimentacao([], [])
            autorizado = Status.objects.filter(autorizado=True)[0]
            perfis = request.user.perfil.setor.internos.all()
            resultado = []

            for perfil in perfis:
                bancos = perfil.movimentacoes.filter(entrada=True, status=autorizado)
                baixas = perfil.movimentacoes.filter(entrada=False, status=autorizado)
                resultado.append(
                    {
                        "nome": perfil.nome,
                        "total_horas": int(
                            funcionalidade.total_de_horas_disponivel_do_perfil(
                                autorizado, bancos, baixas
                            ).split(":")[0]
                        ),
                    }
                )

            return resultado

        except Exception:
            return []


class SolicitacaoBancoDeHorasView(View):
    template_name = "movimentacao/usuario-bancodehoras.html"

    def get(self, request):
        dados = seleciona_dados(request)

        # Sistema de paginação
        paginacao = Paginator(
            request.user.perfil.movimentacoes.all()
            .filter(entrada=True)
            .order_by("data_cadastro")[::-1],
            5,
        )
        page = request.GET.get("pagina")

        try:
            dados["solicitacoes"] = paginacao.get_page(page)
        except:
            dados["solicitacoes"] = paginacao.page(1)
            if page is not None:
                messages.add_message(
                    request, messages.INFO, "A página {} não existe".format(page)
                )

        return render(request, self.template_name, dados)

    def post(self, request):
        solicitante = request.user.perfil
        data_movimentacao = request.POST.get("data")
        hora_inicial = request.POST.get("hora_inicial")
        hora_final = request.POST.get("hora_final")
        motivo = request.POST.get("motivo")

        format_data = FormataDados()

        if (
            len(data_movimentacao) == 0
            or len(hora_inicial) == 0
            or len(hora_final) == 0
            or len(motivo) == 0
        ):
            messages.add_message(
                request,
                messages.WARNING,
                "Todos os campos devem ser preenchidos",
            )
            return redirect("solicitacoes")

        try:
            chave = constant.VALOR_HORA
            valor_hora = Hash.objects.filter(chave=chave)[0].valor
            multiplo = float(valor_hora)
            hora_total = format_data.calcular_hora(
                hora_inicial,
                hora_final,
                multiplo,
            )
            data_movimentacao_formatada = datetime.strptime(
                data_movimentacao, "%Y-%m-%d"
            ).date()

            movimentacao = SolicitacaoHoras(
                data_movimentacao=data_movimentacao_formatada,
                hora_inicial=hora_inicial,
                hora_final=hora_final,
                hora_total=hora_total,
                motivo=motivo,
                status=Movimentacao.ANALISE,
                colaborador=solicitante,
            )
            movimentacao.save()

            log = f"Solicitação realizada com sucesso, solicitação de número: {movimentacao.id}"

            LogSolicitacaoHoras.objects.create(
                log=log,
                perfil_emissor=solicitante,
                movimentacao=movimentacao,
            )

            messages.add_message(
                request, messages.INFO, "Banco de horas solicitado com sucesso."
            )
            return redirect("solicitacoes")
        except OperationalError:
            messages.add_message(
                request,
                messages.INFO,
                "Erro inesperado, contate o administrador e verifique se as configurações do sistema estão corretas.",
            )
            return redirect("solicitacoes")


class SolicitacaoBaixaView(View):
    template_name = "movimentacao/usuario-folga.html"

    def get(self, request):
        dados = seleciona_dados(request)

        # Sistema de paginação
        paginacao = Paginator(
            request.user.perfil.movimentacoes.all()
            .filter(entrada=False)
            .order_by("data_cadastro")[::-1],
            5,
        )
        page = request.GET.get("pagina")

        try:
            dados["solicitacoes"] = paginacao.get_page(page)
        except Exception:
            dados["solicitacoes"] = paginacao.page(1)
            if page is not None:
                messages.add_message(
                    request, messages.INFO, "A página {} não existe".format(page)
                )
        return render(request, self.template_name, dados)

    def post(self, request):
        solicitante = request.user.perfil
        data_folga = request.POST.get("data_folga")
        total_horas = request.POST.get("horas_total")

        if len(data_folga) == 0 or len(total_horas) == 0:
            messages.add_message(request, messages.INFO, "Preencha todos os campos.")
            return redirect("solicitacoes")

        try:
            # Verifica saldo de horas
            funcionalidade = FormataDados()
            dados = seleciona_dados(request)

            if total_horas == "total":
                horas_solicitadas = funcionalidade.converte_hora_em_minutos(
                    str(request.user.perfil.primeiro_horario)
                ) + funcionalidade.converte_hora_em_minutos(
                    str(request.user.perfil.segundo_horario)
                )
            else:
                horas_solicitadas = funcionalidade.converte_hora_em_minutos(total_horas)

            horas_disponiveis = funcionalidade.converte_hora_em_minutos(
                dados["horas_disponiveis"]
            )

            if horas_solicitadas > horas_disponiveis:
                messages.add_message(
                    request,
                    messages.INFO,
                    "Você não possui horas disponívies.",
                )
            else:
                SolicitacaoPagamento.objects.create(
                    data_movimentacao=data_folga,
                    hora_total=funcionalidade.converter_minutos_em_horas(
                        horas_solicitadas,
                    ),
                    status=Movimentacao.ANALISE,
                    colaborador=solicitante,
                )

                messages.add_message(
                    request, messages.INFO, "Baixa solicitada com sucesso."
                )
            return redirect("solicitacoes")

        except Exception:
            messages.add_message(request, messages.INFO, "Preencha todos os campos.")
            return redirect("solicitacoes")


###
# Solicitações do colaborador
###
@login_required(login_url="login")
def solicitacao(request):
    template_name = "movimentacao/solicitacao.html"
    dados = seleciona_dados(request)
    return render(request, template_name, dados)


@login_required(login_url="login")
def listar_solicitacoes(request, id):
    tamplate_name = "movimentacao/listagem-solicitacoes.html"
    dados = seleciona_dados(request)

    # Sistema de paginação
    paginacao = Paginator(
        User.objects.get(username=id).perfil.solicitacoes_horas.all()[::-1], 15
    )
    page = request.GET.get("pagina")
    dados["username"] = id

    try:
        dados["solicitacoes"] = paginacao.get_page(page)
    except Exception:
        dados["solicitacoes"] = paginacao.page(1)
        if page is not None:
            messages.add_message(
                request, messages.INFO, "A página {} não existe".format(page)
            )

    return render(request, tamplate_name, dados)


@login_required(login_url="login")
def solicitacao_mostra_view(request, id):
    template_name = "movimentacao/mostra-solicitacao.html"

    if request.method == "POST":
        try:
            status = int(request.POST.get("id_status"))
            id_movimentacao = int(request.POST.get("id_movimentacao"))
            descricao = request.POST.get("descricao")

            pagamento = None
            if request.POST.get("id_pagamento"):
                id_pagamento = int(request.POST.get("id_pagamento"))
                pagamento = FormaPagamento.objects.get(id=id_pagamento)

            movimentacao = SolicitacaoHoras.objects.get(id=id_movimentacao)
            movimentacao.status = status
            movimentacao.forma_de_pagamento = pagamento
            movimentacao.save()

            perfil = request.user.perfil
            msg_padrao = f"{descricao}"

            LogSolicitacaoHoras.objects.create(
                log=msg_padrao,
                perfil_emissor=perfil,
                movimentacao=movimentacao,
            )
        except Exception:
            messages.add_message(
                request, messages.INFO, "Erro ao modificar solicitação."
            )

    dados = seleciona_dados(request)
    dados["solicitacao"] = Movimentacao.objects.get(id=id)
    return render(request, template_name, dados)


@login_required(login_url="login")
def solciitacao_finaliza(request, id):
    func = FuncionalidadesCore()
    if not func.administardor(request):
        return redirect("solicitacoes")

    movimentacao = Movimentacao.objects.get(id=id)
    analise = Status.objects.filter(analise=True)[0]

    if movimentacao.status == analise:
        messages.add_message(
            request,
            messages.INFO,
            "Impossível finalizar uma movimentação em análise, por favor verifique o status antes de finalizar.",
        )
    else:
        movimentacao.finalizado = True
        movimentacao.save()
        perfil = request.user.perfil
        msg_padrao = "Solicitação finalizada"
        LogMovimentacao.objects.create(
            log=msg_padrao, perfil_emissor=perfil, movimentacao=movimentacao
        )

    return redirect("solicitacoes_mostrar", id=id)


def seleciona_dados(request):
    dados = {}
    now = datetime.now()
    perfil = request.user.perfil

    bancos = perfil.solicitacoes_horas.filter(
        Q(status=Movimentacao.DEFERIDO),
    )
    baixas = perfil.solicitacoes_pagamentos.filter(
        Q(status=Movimentacao.DEFERIDO),
    )
    todos_os_bancos = SolicitacaoHoras.objects.filter(
        status=Movimentacao.DEFERIDO,
    )
    todos_as_baixas = SolicitacaoPagamento.objects.filter(
        status=Movimentacao.DEFERIDO,
    )
    meus_bancos = perfil.solicitacoes_horas.filter(
        status=Movimentacao.DEFERIDO,
    )
    minhas_baixas = perfil.solicitacoes_pagamentos.filter(
        status=Movimentacao.DEFERIDO,
    )
    baixas_pendentes = perfil.solicitacoes_pagamentos.all().filter(
        status=Movimentacao.ANALISE,
    )
    bancos_pendentes = perfil.solicitacoes_horas.filter(
        status=Movimentacao.ANALISE,
    )

    # Dados usuario logado
    format_logado = FuncionalidadesMovimentacao(meus_bancos, minhas_baixas)
    horas_disponiveis = format_logado.total_de_horas_disponivel(
        Movimentacao.DEFERIDO,
    )

    # Dados outros usuarios
    format_dada = FuncionalidadesMovimentacao(todos_os_bancos, todos_as_baixas)
    total_pendentes = len(bancos_pendentes) + len(baixas_pendentes)
    horas_solicitadas = format_dada.calcular_total_de_horas(bancos_pendentes)
    baixas_solicitadas = format_dada.calcular_total_de_horas(baixas_pendentes)
    horas_autorizadas_mes = format_dada.calcular_total_de_horas(
        bancos.filter(data_movimentacao__month=now.month),
    )
    baixas_autorizadas_mes = format_dada.calcular_total_de_horas(
        baixas.filter(data_movimentacao__month=now.month)
    )

    # Formatar dados para retornar
    dados["perfil_logado"] = request.user
    dados["forma_de_pagamento"] = FormaPagamento.objects.all()
    dados["horas_autorizadas"] = format_dada.calcular_total_de_horas(bancos)
    dados["baixas_autorizadas"] = format_dada.calcular_total_de_horas(baixas)
    dados["bancospendentes"] = bancos_pendentes
    dados["baixaspendentes"] = baixas_pendentes
    dados["totalpendente"] = total_pendentes
    dados["horas_disponiveis"] = horas_disponiveis
    dados["horas_solicitadas"] = horas_solicitadas
    dados["baixas_solicitadas"] = baixas_solicitadas
    dados["horas_autorizadas_mes"] = horas_autorizadas_mes
    dados["baixas_autorizadas_mes"] = baixas_autorizadas_mes
    return dados
