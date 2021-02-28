from django.contrib import admin
from core.models import *


class PerfilInline(admin.TabularInline):
    model = Perfil


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ['nome']
    list_filter = ('nome',)
    ordering = ['nome']
    search_fields = ['nome']
    inlines = [PerfilInline]


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['nome', 'gerente', 'ch_primeira', 'ch_segunda', 'display_setor', 'usuario']
    list_filter = ['gerente', 'ch_primeira', 'ch_segunda']
    ordering = ['nome']
    search_fields = ['nome']


# Register your models here.
# admin.site.register(Setor, SetorAdmin)
# admin.site.register(Perfil)
# admin.site.register(Status)
# admin.site.register(FormaDePagamento)
# admin.site.register(Movimentacao)
# admin.site.register(LogMovimentacao)
# admin.site.register(Hash)
