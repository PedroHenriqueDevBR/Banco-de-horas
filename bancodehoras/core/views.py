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
class EscolhaDashboardView(View):
    tamplate_name = 'core/dashboard/opcaodeacesso.html'

    def get(self, request):
        dados = {}
        dados['perfil_logado'] = request.user
        return render(request, self.tamplate_name, dados)    


# Colaborador
class DashboardView(View):
    tamplate_name = 'core/dashboard/dashboard.html'

    def get(self, request):
        dados = {}

        setor = request.user.perfil.setor

        dados['perfil_logado'] = request.user
        dados['colaboradores_do_setor'] = setor.perfis_do_setor.all()
        return render(request, self.tamplate_name, dados)


# Administrador
class AdministradorView(View):
    def get(self, request):
        return redirect('administrador_setor')


class AdministradorSetorView(View):
    tamplate_name = 'core/super/super-setor.html'
    
    def get(self, request):
        dados = {}
        dados['setores'] = Setor.objects.all()
        dados['colaboradores'] = Perfil.objects.all()
        dados['perfil_logado'] = request.user
        return render(request, self.tamplate_name, dados)


class AdministradorMostraSetorView(View):
    tamplate_name = 'core/super/mostra-setor.html'
    
    def get(self, request, id):
        dados = {}
        dados['setor'] = Setor.objects.get(id=id)
        dados['perfil_logado'] = request.user
        return render(request, self.tamplate_name, dados)


class AdministradorMostraUsuarioView(View):
    tamplate_name = 'core/super/mostra-usuario.html'
    
    def get(self, request, id):
        dados = {}
        dados['colaborador'] = User.objects.get(username=id)
        dados['setores'] = Setor.objects.all()
        dados['perfil_logado'] = request.user
        return render(request, self.tamplate_name, dados)


class AdministradorExtraView(View):
    tamplate_name = 'core/super/super-dados-extras.html'

    def get(self, request):
        dados = {}
        dados['perfil_logado'] = request.user
        dados['formasdepagamentos'] = FormaDePagamento.objects.all()
        dados['status'] = Status.objects.all()
        return render(request, self.tamplate_name, dados)


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


class SolicitacaoView(View):
    template_name = 'core/usuario/solicitacao.html'

    def get(self, request):
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
        return render(request, self.template_name, dados)


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

        # import pdb; pdb.set_trace()

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


class PainelDeControleSolicitacoesView(View):
    template_name = 'core/dashboard/dashboard-solicitacoes.html'

    def get(self, request):
        dados = {}
        dados['perfil_logado'] = request.user
        return render(request, self.template_name, dados)


class SetorView(View):
    template_name = 'usuario/cadastrarusuario.html'

    def get(self, request):
        return redirect('administrador_setor')
    
    def post(self, request):
        nome_setor = request.POST.get('nome_setor')
        Setor.objects.create(nome=nome_setor)
        messages.add_message(request, messages.INFO, 'Setor cadastrado com sucesso.')
        return redirect('administrador_setor')


##
### Classes de controle
##
class PermissaoView(View):
    template_name = 'usuario/cadastrarusuario.html'

    
    def get(self, request):
        return redirect('administrador_setor')

    
    def post(self, request):
        nome_permissao = request.POST.get('nome_permissao')
        Permissao.objects.create(nome=nome_permissao)
        return redirect('administrador_setor')


class StatusView(View):
    template_name = 'usuario/cadastrarusuario.html'

    
    def get(self, request):
        return redirect('administrador_extra')

    
    def post(self, request):
        nome_status = request.POST.get('nome_status')
        Status.objects.create(nome=nome_status)
        messages.add_message(request, messages.INFO, 'Status cadastrado com sucesso.')
        return redirect('administrador_extra')


class FormaDePagamentoView(View):
    
    def get(self, request):
        return redirect('administrador_extra')

    
    def post(self, request):
        forma_de_pagamento = request.POST.get('forma_de_pagamento')
        FormaDePagamento.objects.create(nome=forma_de_pagamento)
        messages.add_message(request, messages.INFO, 'Forma de pagamento cadastrada com sucesso.')
        return redirect('administrador_extra')


##
### Deletar e atualizar dados
##
class SetorAtualizaView(View):
    template_name = 'usuario/cadastrarusuario.html'

    def get(self, request):
        return redirect('administrador_setor')

    def post(self, request, id):
        nome = request.POST.get('nome_setor')
        setor = Setor.objects.get(id=id)
        setor.nome = nome
        setor.save()
        return redirect('administrador_setor')


class SetorDeleteView(View):
    template_name = 'usuario/cadastrarusuario.html'

    def get(self, request, id):
        setor = Setor.objects.get(id=id)
        colaboradores = setor.perfis_do_setor.all()

        if colaboradores.count() > 0:
            messages.add_message(request, messages.INFO, 'Impossível deletar, há colaboradores cadastrados no setor selecionado.')
        else:
            messages.add_message(request, messages.INFO, 'Setor deletado com sucesso.')
            setor.delete()

        return redirect('administrador_setor')