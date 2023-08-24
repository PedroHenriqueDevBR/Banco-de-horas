from django.db import models
from apps.usuario.models import Perfil


class FormaPagamento(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name = "Forma de pagamento"
        verbose_name_plural = "Formas de pagamento"


class Movimentacao(models.Model):
    SOLICITADO = 1
    ANALISE = 2
    REVISAO = 3
    DEFERIDO = 3
    INDEFERIDO = 4

    STATUS_MOVIMENTACAO = [
        (SOLICITADO, "Solicitado"),  # Criação da movimentação
        (ANALISE, "Analise"),  # Recebido por um coordenador
        (REVISAO, "Revisao"),  # Solicitante precisa verificar solicitação
        (DEFERIDO, "Deferido"),  # Solicitação autorizada
        (INDEFERIDO, "Indeferido"),  # Solicitação recusada
    ]

    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_movimentacao = models.DateTimeField(auto_now=True)
    motivo = models.TextField(null=True, blank=True)
    status = models.IntegerField(
        choices=STATUS_MOVIMENTACAO,
        default=SOLICITADO,
    )

    def __str__(self):
        return f"{self.data_cadastro}"

    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"


class SolicitacaoHoras(Movimentacao):
    hora_inicial = models.TimeField(null=True, blank=True)
    hora_final = models.TimeField(null=True, blank=True)
    hora_total = models.CharField(max_length=10)
    colaborador = models.ForeignKey(
        Perfil,
        related_name="solicitacoes_horas",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )


class SolicitacaoPagamento(Movimentacao):
    forma_de_pagamento = models.ForeignKey(
        FormaPagamento,
        related_name="pagamento_movimentacoes",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    colaborador = models.ForeignKey(
        Perfil,
        related_name="solicitacoes_pagamentos",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )


class LogMovimentacao(models.Model):
    data = models.DateTimeField(auto_now=True)
    log = models.TextField()
    perfil_emissor = models.ForeignKey(
        Perfil,
        related_name="logs_movimentacao_emitidos",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )


class LogSolicitacaoHoras(LogMovimentacao):
    movimentacao = models.ForeignKey(
        SolicitacaoHoras,
        related_name="log_solicitacoes_horas",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.data} - {self.perfil_emissor.nome}"

    class Meta:
        verbose_name = "Log solicitacao hora"
        verbose_name_plural = "Logs solicitacoes horas"


class LogSolicitacaoPagamento(LogMovimentacao):
    movimentacao = models.ForeignKey(
        SolicitacaoPagamento,
        related_name="log_solicitacoes_pagamentos",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.data} - {self.perfil_emissor.nome}"

    class Meta:
        verbose_name = "Log solicitacao pagamento"
        verbose_name_plural = "Logs solicitacoes pagamento"
