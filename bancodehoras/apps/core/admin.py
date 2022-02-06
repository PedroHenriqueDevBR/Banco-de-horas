from django.contrib import admin
from apps.core.models import *
from django.contrib.auth.models import User


class PerfilInline(admin.TabularInline):
    model = Perfil


class MovimentacoesInline(admin.TabularInline):
    model = Movimentacao
    readonly_fields = [
        'data_cadastro',
        'data_movimentacao',
        'hora_inicial',
        'hora_final',
        'hora_total',
        'motivo',
        'entrada',
        'finalizado',
        'forma_de_pagamento',
        'status',
        'colaborador'
    ]


class LogMovimentacaoInline(admin.TabularInline):
    model = LogMovimentacao
    readonly_fields = ['data', 'log', 'perfil_emissor', 'movimentacao']


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ['nome']
    list_filter = ['nome']
    ordering = ['nome']
    search_fields = ['nome']
    inlines = [PerfilInline]


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['nome', 'gerente', 'ch_primeira', 'ch_segunda', 'display_setor', 'usuario']
    list_filter = ['gerente', 'ch_primeira', 'ch_segunda']
    ordering = ['nome']
    search_fields = ['nome']
    inlines = [MovimentacoesInline]


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['nome', 'analise', 'autorizado']
    list_filter = ['analise', 'autorizado']
    ordering = ['nome']
    search_fields = ['nome']


@admin.register(FormaDePagamento)
class FormaDePagamentoAdmin(admin.ModelAdmin):
    list_display = ['nome']
    ordering = ['nome']
    search_fields = ['nome']


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = [
        'data_cadastro',
        'data_movimentacao',
        'hora_inicial',
        'hora_final',
        'hora_total',
        'motivo',
        'entrada',
        'finalizado',
        'display_forma_de_pagamento',
        'display_status',
        'display_colaborador',
        'display_setor'
    ]
    list_filter = [
        'finalizado'
    ]
    ordering = ['data_cadastro']
    search_fields = ['data_cadastro', 'data_movimentacao']
    inlines = [LogMovimentacaoInline]


@admin.register(LogMovimentacao)
class LogMovimentacao(admin.ModelAdmin):
    list_display = [
        'data',
        'log',
        'display_perfil_emissor',
        'display_movimentaca_data_cadastro',
        'display_movimentaca_colaborador'
    ]
    ordering = [
        'data'
    ]
    search_fields = ['data', 'log']


@admin.register(Hash)
class HashAdmin(admin.ModelAdmin):
    list_display = ['nome', 'chave', 'valor']
    ordering = ['nome']
    search_fields = ['nome', 'chave', 'valor']
