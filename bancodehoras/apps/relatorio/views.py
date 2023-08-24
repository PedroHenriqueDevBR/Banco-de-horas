# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from apps.relatorio import controller
from datetime import datetime
from apps.core.models import *
from apps.movimentacao.views.movimentacao_views import seleciona_dados
import os


# Create your views here.
@login_required(login_url="login")
def relatorio(request):
    if request.method == "POST":
        try:
            data_inicial = request.POST.get("data_inicial")
            data_final = request.POST.get("data_final")
            status = request.POST.get("status")
            andamento = request.POST.get("andamento")
            colaborador = request.POST.get("colaborador")
            forma_pagamento = request.POST.get("forma_pagamento")
            tipo_movimentacao = request.POST.get("tipo_movimentacao")

            inicio = datetime.strptime(data_inicial, "%Y-%m-%d")
            fim = datetime.strptime(data_final, "%Y-%m-%d")
            dados = Movimentacao.objects.filter(data_movimentacao__range=(inicio, fim))
            todas = True

            if status != "0" and status != "":  # Status
                controller.gera_log("Aplicou o filtro de Status")
                id_aux = int(status)
                status = Status.objects.get(id=id_aux)
                dados = dados.filter(status=status)

            if andamento != "0" and andamento != "":  # Andamento da solicitação
                controller.gera_log("Aplicou o filtro de Andamento da solicitação")
                id_aux = False
                if id_aux == "1":
                    id_aux = True
                dados = dados.filter(finalizado=id_aux)

            if colaborador != "0" and colaborador != "":  # colaborador especifico
                controller.gera_log("Aplicou o filtro de Colaborador especifico")
                id_aux = int(colaborador)
                colaborador = Perfil.objects.get(id=id_aux)
                dados = dados.filter(colaborador=colaborador)

            if forma_pagamento != "0" and forma_pagamento != "":  # Forma de pagamento
                controller.gera_log("Aplicou o filtro de Forma de pagamento")
                id_aux = int(forma_pagamento)
                forma_pagamento = FormaDePagamento.objects.get(id=id_aux)
                dados = dados.filter(forma_de_pagamento=forma_pagamento)

            if (
                tipo_movimentacao != "0" and tipo_movimentacao != ""
            ):  # Tipo de movimentacao
                controller.gera_log("Aplicou o filtro de tipo de movimentacao")
                id_aux = False
                if tipo_movimentacao == "1":
                    id_aux = True
                dados = dados.filter(entrada=id_aux)
                todas = False

            res = {}
            if todas:
                res = formata_dados_do_relatorio(dados, todas=todas)
            else:
                res = formata_dados_do_relatorio(
                    dados, tipo_movimentacao=tipo_movimentacao
                )

            username = request.user.username
            filepath = gerador(res, username)
            if os.path.exists(filepath):
                with open(filepath, "rb") as fh:
                    response = HttpResponse(
                        fh.read(), content_type="application/vnd.ms-excel"
                    )
                    response[
                        "Content-Disposition"
                    ] = "inline; filename=" + os.path.basename(filepath)
                    return response

                return HttpResponse("Arquivo não encontrado.")
        except Exception:
            messages.add_message(
                request,
                messages.INFO,
                "Erro ao gerar relatório, verifique se todos "
                + "os campos estão preenchidos corretamente e tente novamente.",
            )

    dados = seleciona_dados(request)
    return render(request, "relatorio/relatorio.html", dados)


def formata_dados_do_relatorio(dados, tipo_movimentacao=None, todas=False):
    if len(dados) == 0:
        res = {"titulos": ["Informação"], "linhas": ["Nenhum resultado localizado"]}

    res = {"titulos": ["Data do cadastro", "Data da movimentação"], "linhas": []}

    if todas:
        controller.gera_log("Listando todos os dados")

        titulos_aux = [
            "Hora inicial",
            "Hora Final",
            "Total de horas",
            "Motivo",
            "Tipo de movimentação",
            "Finalizado",
            "forma de pagamento",
            "Status",
            "Colaborador",
        ]
        res["titulos"] += titulos_aux
        for dado in dados:
            finalizado = "Sim" if dado.finalizado else "Não"
            tipo = "Entrada" if dado.entrada else "Baixa"
            pagamento = dado.forma_de_pagamento.nome if dado.forma_de_pagamento else ""
            res["linhas"].append(
                [
                    formatar_data(str(dado.data_cadastro)),
                    formatar_data(str(dado.data_movimentacao)),
                    str(dado.hora_inicial),
                    str(dado.hora_final),
                    dado.hora_total,
                    dado.motivo,
                    tipo,
                    finalizado,
                    pagamento,
                    dado.status.nome,
                    dado.colaborador.nome,
                ]
            )
    else:
        if tipo_movimentacao == "1":
            controller.gera_log("Listando todos os bancos de horas")

            titulos_aux = [
                "Hora inicial",
                "Hora Final",
                "Total de horas",
                "Motivo",
                "Finalizado",
                "Status",
                "Colaborador",
            ]
            res["titulos"] += titulos_aux
            for dado in dados:
                finalizado = "Sim" if dado.finalizado else "Não"
                res["linhas"].append(
                    [
                        formatar_data(str(dado.data_cadastro)),
                        formatar_data(str(dado.data_movimentacao)),
                        str(dado.hora_inicial),
                        str(dado.hora_final),
                        dado.hora_total,
                        dado.motivo,
                        finalizado,
                        dado.status.nome,
                        dado.colaborador.nome,
                    ]
                )
        else:
            controller.gera_log("Listando todos as baixas")

            titulos_aux = [
                "Total de horas",
                "Forma de pagamento",
                "Finalizado",
                "Status",
                "Colaborador",
            ]
            for dado in dados:
                finalizado = "Sim" if dado.finalizado else "Não"
                pagamento = (
                    dado.forma_de_pagamento.nome if dado.forma_de_pagamento else ""
                )
                res["linhas"].append(
                    [
                        formatar_data(str(dado.data_cadastro)),
                        formatar_data(str(dado.data_movimentacao)),
                        dado.hora_total,
                        pagamento,
                        finalizado,
                        dado.status.nome,
                        dado.colaborador.nome,
                    ]
                )
    return res


def formatar_data(data):
    resultado = data
    if "-" in data:
        data = data.split("-")
        dia = data[2]
        mes = data[1]
        ano = data[0]
        resultado = "{}/{}/{}".format(dia, mes, ano)
    return resultado


def gerador(dados, arquivo_nome="indefinido"):
    pasta = "relatorio/arquivos/"
    nome_arquivo = "{}.xls".format(arquivo_nome)
    arquivo = "{}{}".format(pasta, nome_arquivo)
    filepath = os.path.join(settings.MEDIA_ROOT, arquivo)
    controller.gera_relatorio(dados, arquivo_nome)
    return filepath


@login_required(login_url="login")
def relarorio_de_perfis(request):
    perfis = Perfil.objects.all()
    controller.relatorio_de_usuarios_por_setor(perfis)
    return redirect("dashboard")


@login_required(login_url="login")
def relarorio_de_perfis_baixa(request, arquivo):
    pasta = "relatorio/arquivos/"
    nome_arquivo = arquivo
    arquivo = "{}{}".format(pasta, nome_arquivo)
    filepath = os.path.join(settings.MEDIA_ROOT, arquivo)

    if os.path.exists(filepath):
        with open(filepath, "rb") as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response["Content-Disposition"] = "inline; filename=" + os.path.basename(
                filepath
            )
            return response

    return HttpResponse("Arquivo não encontrado.")


@login_required(login_url="login")
def solicitacoes_pendentes_do_perfil(request):
    # try:
    id = request.user.perfil.id
    perfil = Perfil.objects.get(id=id)
    controller.relatorio_solicitacoes_pendentes_do_perfil(perfil)

    pasta = "relatorio/arquivos/"
    nome_arquivo = "minhas_solicitacoes.xls"
    arquivo = "{}{}".format(pasta, nome_arquivo)
    filepath = os.path.join(settings.MEDIA_ROOT, arquivo)

    if os.path.exists(filepath):
        with open(filepath, "rb") as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response["Content-Disposition"] = "inline; filename=" + os.path.basename(
                filepath
            )
            return response
    else:
        return HttpResponse("Arquivo não encontrado.")

    # except Exception:
    #     messages.add_message(request, messages.INFO, 'Usuário não localizado')
    #     return redirect('dashboard')


@login_required(login_url="login")
def solicitacoes_pendentes_do_meu_setor(request):
    # try:
    user = request.user
    usuarios_do_setor = user.perfil.setor.internos.all()
    controller.relatorio_solicitacoes_do_meu_setor(usuarios_do_setor)

    pasta = "relatorio/arquivos/"
    nome_arquivo = "solicitacoes_do_setor.xls"
    arquivo = "{}{}".format(pasta, nome_arquivo)
    filepath = os.path.join(settings.MEDIA_ROOT, arquivo)

    if os.path.exists(filepath):
        with open(filepath, "rb") as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response["Content-Disposition"] = "inline; filename=" + os.path.basename(
                filepath
            )
            return response
    else:
        return HttpResponse("Arquivo não encontrado.")

    # except Exception:
    #     messages.add_message(request, messages.INFO, 'Usuário não localizado')
    #     return redirect('dashboard')

    # return redirect('dashboard')
