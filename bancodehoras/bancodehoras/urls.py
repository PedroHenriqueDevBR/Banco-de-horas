from django.contrib import admin
from django.urls import path
from core import views as views_core
from usuario import views as views_usuario
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),

    # Core
    path('', login_required(views_core.EscolhaDashboardView.as_view() ,login_url='login'), name='escolha_dashboard'),
    # Cadastros
    path('cadastrarsetor/', login_required(views_core.SetorView.as_view() ,login_url='login'), name='cadastrar_setor'),
    path('cadastrarpermissao/', login_required(views_core.PermissaoView.as_view() ,login_url='login'), name='cadastrar_permissao'),
    path('cadastrarstatus/', login_required(views_core.StatusView.as_view() ,login_url='login'), name='cadastrar_status'),
    path('cadastrarformadepagamento/', login_required(views_core.FormaDePagamentoView.as_view() ,login_url='login'), name='forma_de_pagamento'),
    # Painel de controle do super administrador
    path('administrador/', login_required(views_core.AdministradorView.as_view() ,login_url='login'), name='administrador'),
    path('administrador/setor', login_required(views_core.AdministradorSetorView.as_view() ,login_url='login'), name='administrador_setor'),
    # Painel de controle
    path('paineldecontrole/', login_required(views_core.DashboardView.as_view() ,login_url='login'), name='dashboard'),
    path('paineldecontrole/solicitacoes', login_required(views_core.PainelDeControleSolicitacoesView.as_view() ,login_url='login'), name='dashboard_solicitacoes'),
    # painel de solicitações
    path('solicitacoes/', login_required(views_core.SolicitacaoView.as_view() ,login_url='login'), name='solicitacoes'),
    path('solicitacoes/bancodehoras', login_required(views_core.SolicitacaoBancoDeHorasView.as_view() ,login_url='login'), name='solicitacoes_banco_de_horas'),
    path('solicitacoes/baixas', login_required(views_core.SolicitacaoBaixaView.as_view() ,login_url='login'), name='solicitacoes_baixas'),

    # usuario
    path('login/', views_usuario.LoginUsuarioView.as_view(), name='login'),
    path('logout/', views_usuario.LogoutUsuarioView.as_view(), name='logout'),
    path('cadastrarusuario/', login_required(views_usuario.CadastrarUsuarioView.as_view() ,login_url='login'), name='cadastrar_usuario'),
    path('vincularpermissao/', login_required(views_usuario.ConfiguraAutorizacaoView.as_view() ,login_url='login'), name='vincular_permissao'),
]
