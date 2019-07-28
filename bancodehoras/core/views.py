from django.shortcuts import render, redirect
from django.views.generic.base import View
from core.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

##
### Administrador
##
class EscolhaDashboardView(View):
    tamplate_name = 'core/dashboard/opcaodeacesso.html'
    
    def get(self, request):
        return render(request, self.tamplate_name)    


# Colaborador
class DashboardView(View):
    tamplate_name = 'core/dashboard/dashboard.html'

    def get(self, request):
        # dados = {
        #     'bancos_solicitados': BancoDeHoras.objects.all()
        # }
        dados = {}
        return render(request, self.tamplate_name, dados)


# Administrador
class AdministradorView(View):
    tamplate_name = 'core/super/controle.html'
    
    def get(self, request):
        return redirect('administrador_setor')


class AdministradorSetorView(View):
    tamplate_name = 'core/super/super-setor.html'
    
    def get(self, request):
        dados = {}
        dados['setores'] = Setor.objects.all()
        dados['colaboradores'] = Perfil.objects.all()
        return render(request, self.tamplate_name, dados)

###
#### Solicitações do colaborador
###
class SolicitacaoView(View):
    template_name = 'core/usuario/solicitacao.html'

    def get(self, request):
        return render(request, self.template_name)


class SolicitacaoBancoDeHorasView(View):
    template_name = 'core/usuario/usuario-bancodehoras.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        data = request.POST.get('data_banco')
        hora_inicial = request.POST.get('hora_inicial_banco')
        hora_final = request.POST.get('hora_final_banco')
        motivo = request.POST.get('motivo_banco')
        status = Status.objects.all()[0]
        solicitante = request.user.perfil

        # BancoDeHoras.objects.create(data=data, 
        #                             hora_inicial=hora_inicial, 
        #                             hora_final=hora_final, 
        #                             motivo=motivo, 
        #                             status=status,
        #                             colaborador=solicitante)

        messages.add_message(request, messages.INFO, 'Banco de horas solicitado com sucesso.')
        return redirect('dashboard')


class SolicitacaoBaixaView(View):
    template_name = 'core/usuario/usuario-folga.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        data = request.POST.get('data_banco')
        hora_inicial = request.POST.get('hora_inicial_banco')
        hora_final = request.POST.get('hora_final_banco')
        motivo = request.POST.get('motivo_banco')
        status = Status.objects.all()[0]
        solicitante = request.user.perfil

        # BancoDeHoras.objects.create(data=data, 
        #                             hora_inicial=hora_inicial, 
        #                             hora_final=hora_final, 
        #                             motivo=motivo, 
        #                             status=status,
        #                             colaborador=solicitante)

        messages.add_message(request, messages.INFO, 'Banco de horas solicitado com sucesso.')
        return redirect('dashboard')


class PainelDeControleSolicitacoesView(View):
    template_name = 'core/dashboard/dashboard-solicitacoes.html'

    def get(self, request):
        return render(request, self.template_name)



##
### Classes de controle
##
class SetorView(View):
    template_name = 'usuario/cadastrarusuario.html'

    
    def get(self, request):
        return redirect('cadastrar_usuario')

    
    def post(self, request):
        nome_setor = request.POST.get('nome_setor')
        Setor.objects.create(nome=nome_setor)
        messages.add_message(request, messages.INFO, 'Setor cadastrado com sucesso.')
        return redirect('cadastrar_usuario')


class PermissaoView(View):
    template_name = 'usuario/cadastrarusuario.html'

    
    def get(self, request):
        return redirect('cadastrar_usuario')

    
    def post(self, request):
        nome_permissao = request.POST.get('nome_permissao')
        Permissao.objects.create(nome=nome_permissao)
        return redirect('cadastrar_usuario')


class StatusView(View):
    template_name = 'usuario/cadastrarusuario.html'

    
    def get(self, request):
        return redirect('cadastrar_usuario')

    
    def post(self, request):
        nome_status = request.POST.get('nome_status')
        Status.objects.create(nome=nome_status)
        messages.add_message(request, messages.INFO, 'Status cadastrado com sucesso.')
        return redirect('cadastrar_usuario')


class FormaDePagamentoView(View):
    
    def get(self, request):
        return redirect('cadastrar_usuario')

    
    def post(self, request):
        forma_de_pagamento = request.POST.get('forma_de_pagamento')
        FormaDePagamento.objects.create(nome=forma_de_pagamento)
        messages.add_message(request, messages.INFO, 'Forma de pagamento cadastrada com sucesso.')
        return redirect('cadastrar_usuario')