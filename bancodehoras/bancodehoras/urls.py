from django.contrib import admin
from django.urls import path
from core import views as views_core
from usuario import views as views_usuario

urlpatterns = [
    path('admin/', admin.site.urls),

    # Core
    path('cadastrarsetor/', views_core.SetorView.as_view(), name='cadastrar_setor'),
    path('cadastrarpermissao/', views_core.PermissaoView.as_view(), name='cadastrar_permissao'),
    path('vincularpermissao/', views_core.VincularPermissaoView.as_view(), name='vincular_permissao'),

    # usuario
    path('cadastrarusuario/', views_usuario.CadastrarUsuarioView.as_view(), name='cadastrar_usuario'),
    path('login/', views_usuario.LoginUsuarioView.as_view(), name='login'),
]
