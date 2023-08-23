# from django.contrib import admin
# from apps.usuario.models import Setor, Perfil
# from apps.movimentacao.models import Movimentacao


# class PerfilInline(admin.TabularInline):
#     model = Perfil


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


# @admin.register(Setor)
# class SetorAdmin(admin.ModelAdmin):
#     list_display = ["nome"]
#     list_filter = ["nome"]
#     ordering = ["nome"]
#     search_fields = ["nome"]
#     inlines = [PerfilInline]


# @admin.register(Perfil)
# class PerfilAdmin(admin.ModelAdmin):
#     list_display = [
#         "nome",
#         "gerente",
#         "ch_primeira",
#         "ch_segunda",
#         "display_setor",
#         "usuario",
#     ]
#     list_filter = ["gerente", "ch_primeira", "ch_segunda"]
#     ordering = ["nome"]
#     search_fields = ["nome"]
#     inlines = [MovimentacoesInline]
