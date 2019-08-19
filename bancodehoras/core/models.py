from django.db import models
from django.contrib.auth.models import User


class Setor(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Perfil(models.Model):
    nome = models.CharField(max_length=100)
    gerente = models.BooleanField(default=False)
    ch_primeira = models.TimeField()
    ch_segunda = models.TimeField()
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name='perfis_do_setor')
    usuario = models.OneToOneField(User, on_delete = models.CASCADE, related_name='perfil')

    def __str__(self):
        return self.usuario.username


class Status(models.Model):
    nome = models.CharField(max_length=50)
    analise = models.BooleanField(default=False)
    autorizado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class FormaDePagamento(models.Model):
    nome = models.CharField(max_length=50)
    valor_duplo = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class Movimentacao(models.Model):
    data_cadastro = models.DateField(auto_now=True)
    data_movimentacao = models.DateField()
    hora_inicial = models.TimeField(null=True, blank=True)
    hora_final = models.TimeField(null=True, blank=True)
    hora_total = models.CharField(max_length=10)
    motivo = models.TextField(null=True, blank=True)
    entrada = models.BooleanField()
    finalizado = models.BooleanField(default=False)
    forma_de_pagamento = models.ForeignKey(FormaDePagamento, on_delete=models.CASCADE, related_name='pagamento_movimentacoes', null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='status_movimentacoes')
    colaborador = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='movimentacoes')

    def __str__(self):
        return str(self.data_cadastro) + ' - ' + self.colaborador.nome


class LogMovimentacao(models.Model):
    data = models.DateTimeField(auto_now=True)
    log = models.TextField()
    perfil_emissor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='logs_movimentacao_emitidos')
    movimentacao = models.ForeignKey(Movimentacao, on_delete=models.CASCADE, related_name='log_movimentacoes')

    def __str__(self):
        return str(self.data) + ' - ' + perfil_emissor.nome

class Hash(models.Model):
    nome = models.CharField(max_length=50)
    chave = models.CharField(max_length=50)
    valor = models.CharField(max_length=50)

    def __str__(self):
        return self.nome + ' - ' + self.chave + ' - ' + self.valor 
