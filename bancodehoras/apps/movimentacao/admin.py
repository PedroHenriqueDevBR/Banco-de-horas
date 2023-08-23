# from django.contrib import admin
# from apps.movimentacao.models import (
#     Movimentacao,
#     LogMovimentacao,
#     FormaPagamento,
# )


# class MovimentacoesInline(admin.TabularInline):
#     model = Movimentacao
#     readonly_fields = [
#         "data_cadastro",
#         "data_movimentacao",
#         "hora_inicial",
#         "hora_final",
#         "hora_total",
#         "motivo",
#         "entrada",
#         "finalizado",
#         "forma_de_pagamento",
#         "status",
#         "colaborador",
#     ]


# class LogMovimentacaoInline(admin.TabularInline):
#     model = LogMovimentacao
#     readonly_fields = ["data", "log", "perfil_emissor", "movimentacao"]


# @admin.register(FormaPagamento)
# class FormaDePagamentoAdmin(admin.ModelAdmin):
#     list_display = ["nome"]
#     ordering = ["nome"]
#     search_fields = ["nome"]


# @admin.register(Movimentacao)
# class MovimentacaoAdmin(admin.ModelAdmin):
#     list_display = [
#         "data_cadastro",
#         "data_movimentacao",
#         "hora_inicial",
#         "hora_final",
#         "hora_total",
#         "motivo",
#         "entrada",
#         "finalizado",
#         "display_forma_de_pagamento",
#         "display_status",
#         "display_colaborador",
#         "display_setor",
#     ]
#     list_filter = ["finalizado"]
#     ordering = ["data_cadastro"]
#     search_fields = ["data_cadastro", "data_movimentacao"]
#     inlines = [LogMovimentacaoInline]


# @admin.register(LogMovimentacao)
# class LogMovimentacaoAdmin(admin.ModelAdmin):
#     list_display = [
#         "data",
#         "log",
#         "display_perfil_emissor",
#         "display_movimentaca_data_cadastro",
#         "display_movimentaca_colaborador",
#     ]
#     ordering = ["data"]
#     search_fields = ["data", "log"]
