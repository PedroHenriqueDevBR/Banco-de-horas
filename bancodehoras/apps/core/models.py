from django.db import models
from django.contrib.auth.models import User


class Setor(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'


class Perfil(models.Model):
    nome = models.CharField(max_length=100)
    gerente = models.BooleanField(default=False)
    ch_primeira = models.TimeField()
    ch_segunda = models.TimeField()
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name='perfis_do_setor')
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')

    def __str__(self):
        return self.usuario.username

    def display_setor(self):
        return ''.join(self.setor.nome)

    display_setor.short_description = 'Setor'

    class Meta:
        verbose_name = 'Colaborador'
        verbose_name_plural = 'Colaboradores'


class Status(models.Model):
    nome = models.CharField(max_length=50)
    analise = models.BooleanField(default=False)
    autorizado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'


class FormaDePagamento(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Forma de pagamento'
        verbose_name_plural = 'Formas de pagamento'


class Movimentacao(models.Model):
    data_cadastro = models.DateField(auto_now=True)
    data_movimentacao = models.DateField()
    hora_inicial = models.TimeField(null=True, blank=True)
    hora_final = models.TimeField(null=True, blank=True)
    hora_total = models.CharField(max_length=10)
    motivo = models.TextField(null=True, blank=True)
    entrada = models.BooleanField()
    finalizado = models.BooleanField(default=False)
    forma_de_pagamento = models.ForeignKey(FormaDePagamento, on_delete=models.CASCADE,
                                           related_name='pagamento_movimentacoes', null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='status_movimentacoes')
    colaborador = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='movimentacoes')

    def __str__(self):
        return str(self.data_cadastro) + ' - ' + self.colaborador.nome

    def display_forma_de_pagamento(self):
        if self.forma_de_pagamento is None:
            return 'Não registrado'
        return ''.join(self.forma_de_pagamento.nome)

    def display_status(self):
        if self.status is None:
            return 'Não registrado'
        return ''.join(self.status.nome)

    def display_colaborador(self):
        if self.status is None:
            return 'Não registrado'
        return ''.join(self.colaborador.nome)

    def display_setor(self):
        if self.colaborador.setor is None:
            return 'Não registrado'
        return self.colaborador.setor.nome

    display_forma_de_pagamento.short_description = 'Pagamento'
    display_status.short_description = 'Status'
    display_colaborador.short_description = 'Colaborador'
    display_colaborador.short_description = 'Setor'

    class Meta:
        verbose_name = 'Movimentação'
        verbose_name_plural = 'Movimentações'
    

class LogMovimentacao(models.Model):
    data = models.DateTimeField(auto_now=True)
    log = models.TextField()
    perfil_emissor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='logs_movimentacao_emitidos')
    movimentacao = models.ForeignKey(Movimentacao, on_delete=models.CASCADE, related_name='log_movimentacoes')

    def __str__(self):
        return str(self.data) + ' - ' + self.perfil_emissor.nome

    def display_perfil_emissor(self):
        if self.perfil_emissor is None:
            return 'Perfil não localizado'
        return self.perfil_emissor.nome

    def display_movimentaca_data_cadastro(self):
        if self.movimentacao is None:
            return 'Movimentação não localizada'
        else:
            if self.movimentacao.data_cadastro is None:
                return 'Data não registrada'
        return self.movimentacao.data_cadastro

    def display_movimentaca_colaborador(self):
        if self.movimentacao is None:
            return 'Movimentação não localizada'
        else:
            if self.movimentacao.data_cadastro is None:
                return 'Colaborador não localizado'
        return self.movimentacao.colaborador.nome

    display_perfil_emissor.short_description = 'Colaborador'
    display_movimentaca_data_cadastro.short_description = 'Data movimentação'
    display_movimentaca_colaborador.short_description = 'criador da movimentação'

    class Meta:
        verbose_name = 'Log de movimentação'
        verbose_name_plural = 'Log de movimentações'


class Hash(models.Model):
    nome = models.CharField(max_length=50)
    chave = models.CharField(max_length=50)
    valor = models.CharField(max_length=50)

    def __str__(self):
        return self.nome + ' - ' + self.chave + ' - ' + self.valor

    class Meta:
        verbose_name = 'Hash'
        verbose_name_plural = 'Hash'
