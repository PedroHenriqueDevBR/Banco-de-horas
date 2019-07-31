from django.contrib import admin
from django.urls import path
from core import views as views_core
from usuario import views as views_usuario
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views_core.EscolhaDashboardView, name='escolha_dashboard'),

    # Painel de controle do super administrador
    path('administrador/', views_core.AdministradorView, name='administrador'),
    path('administrador/setor', views_core.AdministradorSetorView, name='administrador_setor'),
    path('administrador/setor/<int:id>', views_core.AdministradorMostraSetorView, name='administrador_setor_id'),
    path('administrador/setor/cadastro', views_core.SetorView, name='cadastrar_setor'),
    path('administrador/setor/delete/<int:id>', views_core.SetorDeleteView, name='setor_deletar'),
    path('administrador/setor/atualiza/<int:id>', views_core.SetorAtualizaView, name='setor_atualiza'),
    path('administrador/usuario/<str:id>', views_core.AdministradorMostraUsuarioView, name='administrador_usuario_id'),

    path('administrador/extra', views_core.AdministradorExtraView, name='administrador_extra'),
    path('administrador/status/cadastro', views_core.StatusView, name='cadastrar_status'),
    path('administrador/status/tornarpadrao/<int:id>', views_core.StatusTornaPadraoView, name='status_tornar_padrao'),
    path('administrador/status/tornarautorizado/<int:id>', views_core.StatusTornaAutorizadoView, name='status_tornar_autorizado'),
    path('administrador/status/deletar/<int:id>', views_core.StatusDeleteView, name='status_deletar'),
    path('administrador/formadepagamento/cadastro', views_core.FormaDePagamentoView, name='forma_de_pagamento'),
    path('administrador/formadepagamento/deletar/<int:id>', views_core.FormaDePagamentoDeletarView, name='forma_de_pagamento_deletar'),
    
    # Painel de controle
    path('paineldecontrole/', views_core.DashboardView, name='dashboard'),
    path('paineldecontrole/solicitacoes/', views_core.SolicitacaoView, name='solicitacoes'),
    path('paineldecontrole/solicitacoes/mostrar/<int:id>', views_core.SolicitacaoMostrarView, name='solicitacoes_mostrar'),
    path('paineldecontrole/solicitacoes/pendentes', login_required(views_core.PainelDeControleSolicitacoesView.as_view() ,login_url='login'), name='dashboard_solicitacoes'),
    path('paineldecontrole/solicitacoes/bancodehoras', login_required(views_core.SolicitacaoBancoDeHorasView.as_view() ,login_url='login'), name='solicitacoes_banco_de_horas'),
    path('paineldecontrole/solicitacoes/baixas', login_required(views_core.SolicitacaoBaixaView.as_view() ,login_url='login'), name='solicitacoes_baixas'),

    # usuario
    path('login/', views_usuario.LoginUsuarioView.as_view(), name='login'),
    path('logout/', views_usuario.LogoutUsuarioView, name='logout'),
    path('usuario/cadastrar/', views_usuario.CadastrarUsuarioView, name='cadastrar_usuario'),
    path('usuario/atualiza/<str:id>', views_usuario.AtualizarUsuarioView, name='usuario_atualiza'),
    path('usuario/atualiza/ativo/<int:id>', views_usuario.UsuarioAtivoView, name='usuario_ativo'),
    path('usuario/atualiza/gerente/<int:id>', views_usuario.UsuarioGerenteView, name='usuario_gerente'),
    path('usuario/atualiza/administrador/<int:id>', views_usuario.UsuarioAdministradorView, name='usuario_administrador'),

]
