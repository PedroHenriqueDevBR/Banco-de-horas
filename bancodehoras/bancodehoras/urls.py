from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from core import views as views_core
from movimentacao import views as views_mov
from relatorio import views as views_rel
from usuario import views as views_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views_core.dashboard, name='escolha_dashboard'),
    path('installsystem', views_core.isntalar_sistema, name='install_system'),

    # Relatórios
    path('relatorio/', views_rel.relatorio, name='relatorio'),
    path('relatorio/solicitacoesdoperfil/<int:id>', views_rel.solicitacoes_pendentes_do_perfil, name='rel_solicitacoes_do_perfil'),
    path('relatorio/solicitacoesdosetor/', views_rel.solicitacoes_pendentes_do_meu_setor, name='rel_solicitacoes_do_setor'),

    # Painel de controle do super administrador
    path('administrador/', views_core.administrador, name='administrador'),
    path('administrador/setor', views_core.setor, name='setor'),
    path('administrador/setor/selecionar/<int:id>', views_core.administrador_mostra_setor, name='administrador_setor_id'),
    path('administrador/setor/deletar/<int:id>', views_core.setor_delete, name='setor_deletar'),
    path('administrador/setor/atualizar/<int:id>', views_core.setor_atualiza, name='setor_atualiza'),

    path('administrador/extra', views_core.administrador_extra, name='administrador_extra'),
    path('administrador/extra/modificarconfiguracao/<int:id>', views_core.hash_edit, name='hash'),
    path('administrador/status/cadastrar', views_core.status, name='cadastrar_status'),
    path('administrador/status/padronizar/analise/<int:id>', views_core.status_torna_padrao_analise, name='status_tornar_padrao_analise'),
    path('administrador/status/padronizar/autorizado/<int:id>', views_core.status_torna_padrao_autorizado, name='status_tornar_padrao_autorizado'),
    path('administrador/status/editar/<int:id>', views_core.status_editar, name='status_editar'),
    path('administrador/status/deletar/<int:id>', views_core.status_delete, name='status_deletar'),
    path('administrador/formadepagamento/cadastrar', views_core.forma_de_pagamento, name='forma_de_pagamento'),
    path('administrador/formadepagamento/editar/<int:id>', views_core.forma_de_pagamento_editar, name='forma_de_pagamento_editar'),
    path('administrador/formadepagamento/deletar/<int:id>', views_core.forma_de_pagamento_delete, name='forma_de_pagamento_deletar'),
    
    # Painel de controle
    path('paineldecontrole/', views_core.dashboard, name='dashboard'),
    path('paineldecontrole/solicitacoes/', views_mov.solicitacao, name='solicitacoes'),
    path('paineldecontrole/solicitacoes/listartodas/<str:id>/', views_mov.listar_solicitacoes, name='listar_solicitacoes'),
    path('paineldecontrole/solicitacoes/selecionar/<int:id>', views_mov.solicitacao_mostra_view, name='solicitacoes_mostrar'),
    path('paineldecontrole/solicitacoes/finalizar/<int:id>', views_mov.solciitacao_finaliza, name='solicitacoes_finalizar'),
    path('paineldecontrole/solicitacoes/bancodehoras/pendentes/', login_required(views_mov.PainelDeControleSolicitacoesView.as_view() ,login_url='login'), name='dashboard_solicitacoes'),
    path('paineldecontrole/solicitacoes/baixas/pendentes/', login_required(views_mov.PainelDeControleFolgasView.as_view() ,login_url='login'), name='dashboard_baixas'),
    path('paineldecontrole/solicitacoes/bancodehoras/', login_required(views_mov.SolicitacaoBancoDeHorasView.as_view() ,login_url='login'), name='solicitacoes_banco_de_horas'),
    path('paineldecontrole/solicitacoes/baixas/', login_required(views_mov.SolicitacaoBaixaView.as_view() ,login_url='login'), name='solicitacoes_baixas'),

    # usuario
    path('login/', views_usuario.LoginUsuarioView.as_view(), name='login'),
    path('logout/', views_usuario.logout_usuario, name='logout'),
    path('usuario/cadastrar/', views_usuario.cadastrar_usuario, name='cadastrar_usuario'),
    path('usuario/seleciona/<str:id>', views_usuario.atualiza_usuario, name='usuario_atualiza'),
    path('usuario/atualiza/ativo/<int:id>', views_usuario.usuario_ativo, name='usuario_ativo'),
    path('usuario/atualiza/gerente/<int:id>', views_usuario.usuario_gerente, name='usuario_gerente'),
    path('usuario/atualiza/administrador/<int:id>', views_usuario.usuario_administrador, name='usuario_administrador'),
]
