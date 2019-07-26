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
    nome = models.CharField(max_length = 100)


class UsuarioPermissao(models.Model):
    permissao = models.ForeignKey(Permissao, on_delete=models.CASCADE, related_name='usuarios_selecionados')
    perfil_emissor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='permissoes_emitidas')
    perfil_receptor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='permissoes_recebidas')
    data_alteracao = models.DateTimeField(auto_now=True)


class Status(models.Model):
    nome = models.CharField(max_length=50)


class BancoDeHoras(models.Model):
    data = models.DateTimeField(auto_now=True)
    hora_inicial = models.TimeField()
    hora_final = models.TimeField()
    motivo = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='bancos')
    colaborador = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='banco_de_horas')


class LogBancoDeHoras(models.Model):
    perfil_emissor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='logs_banco_emitidos')
    banco_de_horas = models.ForeignKey(BancoDeHoras, on_delete=models.CASCADE, related_name='log_banco_de_horas')
    data = models.DateTimeField(auto_now=True)
    log = models.TextField()


class FormaDePagamento(models.Model):
    nome = models.CharField(max_length=50)


class Baixa(models.Model):
    data_cadastro = models.DateField()
    data_baixa = models.DateField()
    quantidade_de_horas = models.IntegerField()
    forma_de_pagamento = models.ForeignKey(FormaDePagamento, on_delete=models.CASCADE, related_name='forma_de_pagamento_baixa')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='baixas_do_status')
    colaborador = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='baixas_do_perfil')


class LogBaixa(models.Model):
    perfil_emissor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='logs_baixa_emitidos')
    banco_de_horas = models.ForeignKey(BancoDeHoras, on_delete=models.CASCADE, related_name='log_baixas')
    data = models.DateTimeField(auto_now=True)
    log = models.TextField()
