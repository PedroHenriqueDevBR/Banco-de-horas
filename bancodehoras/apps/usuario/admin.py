from django.contrib import admin
from apps.usuario.models import Setor, Perfil, Unidade


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ["nome"]
    list_filter = ["nome"]
    ordering = ["nome"]
    search_fields = ["nome"]


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ["nome", "unidade"]
    list_filter = ["nome"]
    ordering = ["nome"]
    search_fields = ["nome"]


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = [
        "nome",
        "gerente",
        "primeiro_horario",
        "segundo_horario",
        "setor",
        "usuario",
    ]
    list_filter = ["gerente", "primeiro_horario", "segundo_horario"]
    ordering = ["nome"]
    search_fields = ["nome"]
