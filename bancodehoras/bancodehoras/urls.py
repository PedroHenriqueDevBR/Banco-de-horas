from django.contrib import admin
from django.urls import path
from core import views as views_core
from usuario import views as views_usuario
from movimentacao import views as views_mov
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views_core.dashboard, name='escolha_dashboard'),

    # Painel de controle do super administrador
    path('administrador/', views_core.administrador, name='administrador'),
    path('administrador/setor', views_core.administrador_setor, name='administrador_setor'),
    path('administrador/setor/<int:id>', views_core.administrador_mostra_setor, name='administrador_setor_id'),
    path('administrador/setor/cadastro', views_core.setor, name='cadastrar_setor'),
    path('administrador/setor/delete/<int:id>', views_core.setor_delete, name='setor_deletar'),
    path('administrador/setor/atualiza/<int:id>', views_core.setor_atualiza, name='setor_atualiza'),
    path('administrador/usuario/<str:id>', views_core.administrador_mostra_usuario, name='administrador_usuario_id'),

    path('administrador/extra', views_core.administrador_extra, name='administrador_extra'),
    path('administrador/status/cadastro', views_core.status, name='cadastrar_status'),
    path('administrador/status/tornarpadrao/analise/<int:id>', views_core.status_torna_padrao_analise, name='status_tornar_padrao_analise'),
    path('administrador/status/tornarpadrao/autorizado/<int:id>', views_core.status_torna_padrao_autorizado, name='status_tornar_padrao_autorizado'),
    path('administrador/status/deletar/<int:id>', views_core.status_delete, name='status_deletar'),
    path('administrador/formadepagamento/cadastro', views_core.forma_de_pagamento, name='forma_de_pagamento'),
    path('administrador/formadepagamento/deletar/<int:id>', views_core.forma_de_pagamento_delete, name='forma_de_pagamento_deletar'),
    
    # Painel de controle
    path('paineldecontrole/', views_core.dashboard, name='dashboard'),
    path('paineldecontrole/solicitacoes/', views_mov.solicitacao, name='solicitacoes'),
    path('paineldecontrole/solicitacoes/listartodos/<str:id>', views_mov.listar_solicitacoes, name='listar_solicitacoes'),
    path('paineldecontrole/solicitacoes/mostrar/<int:id>', views_mov.solicitacao_mostra_view, name='solicitacoes_mostrar'),
    path('paineldecontrole/solicitacoes/finalizar/<int:id>', views_mov.solciitacao_finaliza, name='solicitacoes_finalizar'),
    path('paineldecontrole/solicitacoes/pendentes', login_required(views_mov.PainelDeControleSolicitacoesView.as_view() ,login_url='login'), name='dashboard_solicitacoes'),
    path('paineldecontrole/baixas/pendentes', login_required(views_mov.PainelDeControleFolgasView.as_view() ,login_url='login'), name='dashboard_baixas'),
    path('paineldecontrole/solicitacoes/bancodehoras', login_required(views_mov.SolicitacaoBancoDeHorasView.as_view() ,login_url='login'), name='solicitacoes_banco_de_horas'),
    path('paineldecontrole/solicitacoes/baixas', login_required(views_mov.SolicitacaoBaixaView.as_view() ,login_url='login'), name='solicitacoes_baixas'),

    # usuario
    path('login/', views_usuario.LoginUsuarioView.as_view(), name='login'),
    path('logout/', views_usuario.logout_usuario, name='logout'),
    path('usuario/cadastrar/', views_usuario.cadastrar_usuario, name='cadastrar_usuario'),
    path('usuario/atualiza/<str:id>', views_usuario.atualiza_usuario, name='usuario_atualiza'),
    path('usuario/atualiza/ativo/<int:id>', views_usuario.usuario_ativo, name='usuario_ativo'),
    path('usuario/atualiza/gerente/<int:id>', views_usuario.usuario_gerente, name='usuario_gerente'),
    path('usuario/atualiza/administrador/<int:id>', views_usuario.usuario_administrador, name='usuario_administrador'),
]
