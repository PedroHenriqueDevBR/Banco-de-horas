from django.shortcuts import render, redirect
from django.views.generic.base import View
from core.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime

##
### Administrador
##
def EscolhaDashboardView(request):
    tamplate_name = 'core/dashboard/opcaodeacesso.html'
    dados = {}
    dados['perfil_logado'] = request.user
    return render(request, tamplate_name, dados)    


# Colaborador
def DashboardView(request):
    tamplate_name = 'core/dashboard/dashboard.html'
    dados = {}

    setor = request.user.perfil.setor

    dados['perfil_logado'] = request.user
    dados['colaboradores_do_setor'] = setor.perfis_do_setor.all()
    return render(request, tamplate_name, dados)


# Gerente
class PainelDeControleSolicitacoesView(View):
    template_name = 'core/dashboard/dashboard-solicitacoes.html'

    def get(self, request):
        dados = {}
        dados['perfil_logado'] = request.user
        dados['solciitacoes_pendentes'] = self.seleciona_todas_movimentacoes(request.user.perfil.setor.perfis_do_setor.all())
        return render(request, self.template_name, dados)

    def seleciona_todas_movimentacoes(self, perfis):
        movimentacoes = []
        analise = Status.objects.all()[0]
        for perfil in perfis:
            movimentacoes.extend(
                perfil.movimentacoes.all().filter(
                    Q(status=analise),
                    Q(eh_entrada=True)
                )
            )
        return movimentacoes


# Administrador
def AdministradorView(request):
    return redirect('administrador_setor')


def AdministradorSetorView(request):
    tamplate_name = 'core/super/super-setor.html'
    dados = {}
    dados['setores'] = Setor.objects.all()
    dados['colaboradores'] = Perfil.objects.all()
    dados['perfil_logado'] = request.user
    return render(request, tamplate_name, dados)


def AdministradorMostraSetorView(request, id):
    tamplate_name = 'core/super/mostra-setor.html'
    dados = {}
    dados['setor'] = Setor.objects.get(id=id)
    dados['perfil_logado'] = request.user
    return render(request, tamplate_name, dados)


def AdministradorMostraUsuarioView(request, id):
    tamplate_name = 'core/super/mostra-usuario.html'
    dados = {}
    dados['colaborador'] = User.objects.get(username=id)
    dados['setores'] = Setor.objects.all()
    dados['perfil_logado'] = request.user
    return render(request, tamplate_name, dados)


def AdministradorExtraView(request):
    tamplate_name = 'core/super/super-dados-extras.html'
    dados = {}
    dados['perfil_logado'] = request.user
    dados['formasdepagamentos'] = FormaDePagamento.objects.all()
    dados['status'] = Status.objects.all()
    return render(request, tamplate_name, dados)


###
#### Solicitações do colaborador
###
class FormataDados:
    def calcular_hora(self, inicio, fim):
        if ':' not in inicio or ':' not in fim:
            return 0

        hora_inicio = self.converte_hora_em_minutos(inicio)
        hora_final = self.converte_hora_em_minutos(fim)

        if hora_inicio > hora_final:
            return 0
        else:
            return self.converter_minutos_em_horas(hora_final - hora_inicio)


    def converte_hora_em_minutos(self, hora_completa):
        if ':' not in hora_completa:
            return 0
        
        horas = int(hora_completa.split(':')[0]) * 60
        minutos = int(hora_completa.split(':')[1])

        return horas + minutos


    def converter_minutos_em_horas(self, minutos):
        if minutos >= 60:
            horas = minutos // 60
            minutos = minutos - (horas * 60)
        else:
            horas = 0
            minutos

        hora_str = '{}'.format(horas)
        if horas < 10:
            hora_str = '0{}'.format(horas)

        min_str = '{}'.format(minutos)
        if minutos < 10:
            min_str = '0{}'.format(minutos)

        return '{}:{}'.format(hora_str, min_str)

    def calcular_total_de_horas(self, obj):
        total_min = 0
        # import pdb; pdb.set_trace()
        for movimentacao in obj:
            total_min += self.converte_hora_em_minutos(movimentacao.hora_total)
        return self.converter_minutos_em_horas(total_min)


def SolicitacaoView(request):
    template_name = 'core/usuario/solicitacao.html'
    dados = {}
    analise = Status.objects.all()[0]
    autorizado = Status.objects.all()[1]
    format_data = FormataDados()
    
    dados['perfil_logado'] = request.user
    dados['bancospendentes'] = request.user.perfil.movimentacoes.all().filter(
        Q(status=analise),
        Q(eh_entrada=True)
    )
    dados['baixaspendentes'] = request.user.perfil.movimentacoes.all().filter(
        Q(status=analise),
        Q(eh_entrada=False)
    )
    dados['total_de_banco_solicitado'] = format_data.calcular_total_de_horas(dados['bancospendentes'])
    dados['total_de_baixa_solicitado'] = format_data.calcular_total_de_horas(dados['baixaspendentes'])
    return render(request, template_name, dados)


class SolicitacaoBancoDeHorasView(View):
    template_name = 'core/usuario/usuario-bancodehoras.html'

    def get(self, request):
        dados = {}
        dados['perfil_logado'] = request.user
        dados['solicitacoes'] = request.user.perfil.movimentacoes.all().filter(eh_entrada=True)
        return render(request, self.template_name, dados)

    def post(self, request):
        data_movimentacao = request.POST.get('data')
        hora_inicial = request.POST.get('hora_inicial')
        hora_final = request.POST.get('hora_final')
        motivo = request.POST.get('motivo')
        status = Status.objects.all()[0]
        solicitante = request.user.perfil
        format_data = FormataDados()
        hora_total = format_data.calcular_hora(hora_inicial, hora_final)
        data_movimentacao_formatada = datetime.strptime(data_movimentacao, '%Y-%m-%d').date()

        Movimentacao.objects.create(
            data_movimentacao=data_movimentacao_formatada,
            hora_inicial = hora_inicial,
            hora_final = hora_final,
            hora_total = hora_total,
            motivo = motivo,
            status = status,
            eh_entrada = True,
            colaborador = solicitante
        )

        messages.add_message(request, messages.INFO, 'Banco de horas solicitado com sucesso.')
        return redirect('solicitacoes')


class SolicitacaoBaixaView(View):
    template_name = 'core/usuario/usuario-folga.html'

    def get(self, request):
        dados = {}
        dados['perfil_logado'] = request.user
        dados['solicitacoes'] = request.user.perfil.movimentacoes.all().filter(eh_entrada=False)
        return render(request, self.template_name, dados)

    def post(self, request):
        data_folga = request.POST.get('data_folga')
        total_horas = request.POST.get('horas_total')
        status = Status.objects.all()[0]
        solicitante = request.user.perfil
        total_horas = '0{}:00'.format(total_horas) if int(total_horas) < 10 else '{}:00'.format(total_horas)

        Movimentacao.objects.create(
            data_movimentacao=data_folga,
            eh_entrada=False,
            hora_total=total_horas,
            status = status,
            colaborador = solicitante
        )

        messages.add_message(request, messages.INFO, 'Baixa solicitada com sucesso.')
        return redirect('solicitacoes')


# Setor
def SetorView(request):
    nome_setor = request.POST.get('nome_setor')
    Setor.objects.create(nome=nome_setor)
    messages.add_message(request, messages.INFO, 'Setor cadastrado com sucesso.')
    return redirect('administrador_setor')


def SetorAtualizaView(request, id):
    nome = request.POST.get('nome_setor')
    setor = Setor.objects.get(id=id)
    setor.nome = nome
    setor.save()
    return redirect('administrador_setor')


def SetorDeleteView(request, id):
    setor = Setor.objects.get(id=id)
    colaboradores = setor.perfis_do_setor.all()

    if colaboradores.count() > 0:
        messages.add_message(request, messages.INFO, 'Impossível deletar, há colaboradores cadastrados no setor selecionado.')
    else:
        messages.add_message(request, messages.INFO, 'Setor deletado com sucesso.')
        setor.delete()

    return redirect('administrador_setor')


##
### Classes de controle
##
def StatusView(request):
    nome_status = request.POST.get('nome_status')
    Status.objects.create(nome=nome_status)
    messages.add_message(request, messages.INFO, 'Status cadastrado com sucesso.')
    return redirect('administrador_extra')


def FormaDePagamentoView(request):
    forma_de_pagamento = request.POST.get('forma_de_pagamento')
    FormaDePagamento.objects.create(nome=forma_de_pagamento)
    messages.add_message(request, messages.INFO, 'Forma de pagamento cadastrada com sucesso.')
    return redirect('administrador_extra')
