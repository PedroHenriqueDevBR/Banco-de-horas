from django.contrib import admin
from django.urls import path
from core import views as views_core
from usuario import views as views_usuario

urlpatterns = [
    path('admin/', admin.site.urls),

    # Core
    path('cadastrarsetor/', views_core.SetorView.as_view(), name='cadastrar_setor'),
    path('cadastrarpermissao/', views_core.PermissaoView.as_view(), name='cadastrar_permissao'),
    path('cadastrarstatus/', views_core.StatusView.as_view(), name='cadastrar_status'),
    path('cadastrarformadepagamento/', views_core.FormaDePagamentoView.as_view(), name='forma_de_pagamento'),
    path('dashboard/', views_core.DashboardView.as_view(), name='dashboard'),
    path('bancodehoras/', views_core.BancoDeHorasView.as_view(), name='banco_de_horas'),

    # usuario
    path('login/', views_usuario.LoginUsuarioView.as_view(), name='login'),
    path('cadastrarusuario/', views_usuario.CadastrarUsuarioView.as_view(), name='cadastrar_usuario'),
    path('vincularpermissao/', views_usuario.ConfiguraAutorizacaoView.as_view(), name='vincular_permissao'),
]
