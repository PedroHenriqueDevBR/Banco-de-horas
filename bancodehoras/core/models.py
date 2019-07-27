from django.db import models
from django.contrib.auth.models import User


class Setor(models.Model):
    nome = models.CharField(max_length=50)


class Perfil(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=10)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name='perfis_do_setor')
    usuario = models.OneToOneField(User, on_delete = models.CASCADE, related_name='perfil')

    @property
    def email(self):
        return self.usuario.perfil


class Permissao(models.Model):
    cod_permissao = models.CharField(max_length = 20)
    nome = models.CharField(max_length = 100)


class UsuarioPermissao(models.Model):
    permissao = models.ForeignKey(Permissao, on_delete=models.CASCADE, related_name='usuarios_selecionados')
    perfil_emissor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='permissoes_emitidas')
    perfil_receptor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='permissoes_recebidas')
    data_alteracao = models.DateTimeField(auto_now=True)


class Status(models.Model):
    nome = models.CharField(max_length=50)


class FormaDePagamento(models.Model):
    nome = models.CharField(max_length=50)


class Movimentacao(models.Model):
    data_cadastro = models.DateField(auto_now=True)
    data_movimentacao = models.DateField(auto_now=True)
    hora_inicial = models.TimeField()
    hora_final = models.TimeField()
    motivo = models.TextField()
    forma_de_pagamento = models.ForeignKey(FormaDePagamento, on_delete=models.CASCADE, related_name='pagamento_movimentacoes')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='status_movimentacoes')
    colaborador = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='movimentacoes')


class LogMovimentacao(models.Model):
    perfil_emissor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='logs_movimentacao_emitidos')
    banco_de_horas = models.ForeignKey(Movimentacao, on_delete=models.CASCADE, related_name='log_movimentacoes')
    data = models.DateTimeField(auto_now=True)
    log = models.TextField()
