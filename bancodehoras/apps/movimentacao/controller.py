from apps.movimentacao.models import Movimentacao


class FormataDados:
    def calcular_hora(self, inicio, fim, multiplo):
        if ":" not in inicio or ":" not in fim:
            return 0

        hora_inicio = self.converte_hora_em_minutos(inicio)
        hora_final = self.converte_hora_em_minutos(fim)

        if hora_inicio > hora_final:
            return 0
        else:
            total = int((hora_final - hora_inicio) * multiplo)
            # import pdb; pdb.set_trace()
            return self.converter_minutos_em_horas(total)

    def converte_hora_em_minutos(self, hora_completa):
        if "-" in hora_completa:
            return 0

        if ":" not in hora_completa:
            return 0
        horas = int(hora_completa.split(":")[0]) * 60
        minutos = int(hora_completa.split(":")[1])

        return horas + minutos

    def converter_minutos_em_horas(self, minutos):
        negativo = False
        if minutos < 0:
            minutos = minutos * -1
            negativo = True

        if minutos >= 60:
            horas = minutos // 60
            minutos = minutos - (horas * 60)
        else:
            horas = 0

        hora_str = "{}".format(horas)
        if horas < 10:
            hora_str = "0{}".format(horas)

        min_str = "{}".format(minutos)
        if minutos < 10:
            min_str = "0{}".format(minutos)

        if negativo:
            resultado = "- {}:{}".format(hora_str, min_str)
        else:
            resultado = "{}:{}".format(hora_str, min_str)

        return resultado


class FuncionalidadesMovimentacao:
    bancos = []
    baixas = []
    formatar = object

    def __init__(self, bancos, baixas):
        self.bancos = bancos
        self.baixas = baixas
        self.formatar = FormataDados()

    def total_de_horas_disponivel(self, base):
        total_entrada = 0
        total_saida = 0

        for banco in self.bancos:
            if banco.status == base:
                total_entrada += self.formatar.converte_hora_em_minutos(
                    banco.hora_total,
                )

        for baixa in self.baixas:
            if baixa.status == base:
                total_saida += self.formatar.converte_hora_em_minutos(
                    baixa.hora_total,
                )

        return self.formatar.converter_minutos_em_horas(
            total_entrada - total_saida,
        )

    def total_de_horas_disponivel_do_perfil(self, base, bancos, baixas):
        total_entrada = 0
        total_saida = 0

        for banco in bancos:
            if banco.status == base:
                total_entrada += self.formatar.converte_hora_em_minutos(
                    banco.hora_total
                )

        for baixa in baixas:
            if baixa.status == base:
                total_saida += self.formatar.converte_hora_em_minutos(baixa.hora_total)

        # import pdb; pdb.set_trace()

        return self.formatar.converter_minutos_em_horas(total_entrada - total_saida)

    def calcular_total_de_horas(self, obj):
        total_min = 0
        # import pdb; pdb.set_trace()
        for movimentacao in obj:
            total_min += self.formatar.converte_hora_em_minutos(movimentacao.hora_total)
        return self.formatar.converter_minutos_em_horas(total_min)


class Utilidades:
    def seleciona_todas_movimentacoes(self, perfis, entrada):
        movimentacoes = []
        if entrada:
            for perfil in perfis:
                movimentacoes.extend(
                    perfil.solicitacoes_horas.filter(
                        status=Movimentacao.DEFERIDO,
                    )
                )
        else:
            for perfil in perfis:
                movimentacoes.extend(
                    perfil.solicitacoes_pagamentos.filter(
                        status=Movimentacao.DEFERIDO,
                    )
                )
        return movimentacoes
