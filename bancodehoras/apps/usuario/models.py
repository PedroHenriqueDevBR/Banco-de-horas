from django.db import models
from django.contrib.auth.models import User


class Unidade(models.Model):
    nome = models.CharField(max_length=250)

    def __str__(self) -> str:
        return f"{self.nome}"

    class Meta:
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"


class Setor(models.Model):
    nome = models.CharField(max_length=250)
    unidade = models.ForeignKey(
        Unidade,
        on_delete=models.SET_NULL,
        related_name="setores",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.nome}"

    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"


class Perfil(models.Model):
    nome = models.CharField(max_length=100)
    gerente = models.BooleanField(default=False)
    primeiro_horario = models.TimeField()  # 4:00
    segundo_horario = models.TimeField()  # 4:00
    setor = models.ForeignKey(
        Setor,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="internos",
    )
    usuario = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="perfil",
    )

    def __str__(self):
        return f"{self.nome}"

    def display_setor(self):
        return f"{self.setor}"

    display_setor.short_description = "Setor"

    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"


class ResponsavelSetor(models.Model):
    data_cadastro = models.DateTimeField(auto_now_add=True)
    responsavel = models.ForeignKey(
        Perfil,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    setor = models.ForeignKey(
        Unidade,
        on_delete=models.CASCADE,
        related_name="responsaveis",
    )
    perfil = models.ForeignKey(
        Perfil,
        on_delete=models.CASCADE,
        related_name="responsabilidades",
    )
