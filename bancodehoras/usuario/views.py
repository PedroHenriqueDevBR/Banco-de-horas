from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from core.models import *
from django.contrib import messages 
from usuario.forms import RegistrarUsuarioForm


class CadastrarUsuarioView(View):
    template_name = 'usuario/cadastrarusuario.html'
    
    def get(self, request):
        dados = {
            'setores': Setor.objects.all(),
            'perfis': Perfil.objects.all(),
            'permissoes': Permissao.objects.all()
        }
        return render(request, self.template_name, dados)

    
    def post(self, request):
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            dados_form = form.cleaned_data
            # cadastra usuario
            usuario = User.objects.create_user(username=dados_form['matricula'],
                                                email=dados_form['email'],
                                                password=dados_form['senha'])

            # seleciona o setor de acordo com o id passado no post
            setor = Setor.objects.get(id=dados_form['setor'])

            # cadastra perfil vinculando ao usuario e ao setor
            perfil = Perfil(nome=dados_form['nome'], 
                            usuario=usuario,
                            setor=setor)
            perfil.save()

            messages.add_message(request, messages.INFO, 'Colaborador cadastrado com sucesso')
            return redirect('cadastrar_usuario')

        return render(request, self.template_name, {'form': form})


class AtualizarUsuarioView(View):
    template_name = 'usuario/cadastrarusuario.html'

    def get(self, request):
        return redirect('administrador_usuario_id')
    
    def post(self, request, id):
        nome = request.POST.get('nome')
        matricula = request.POST.get('matricula')
        id_setor = request.POST.get('setor')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = User.objects.get(username=id)
        user.username = matricula
        user.email = email
        perfil = user.perfil
        perfil.nome = nome
        perfil.setor = Setor.objects.get(id=id_setor)

        if senha != '':
            user.set_password(senha)
        
        perfil.save()
        user.save()

        return redirect('administrador_setor')


class LoginUsuarioView(View):
    template_name = 'usuario/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('login')
        password = request.POST.get('senha')

        user = authenticate(username=username, password=password)

        if user is None:
            if User.objects.filter(username=username):
                messages.add_message(request, messages.INFO, 'Usuário inativo.')
            else:
                messages.add_message(request, messages.INFO, 'Colaborador não cadastrado.')
        else:
            messages.add_message(request, messages.INFO, 'Seja bem vindo {}.'.format(user.perfil.nome))
            login(request, user)
            return redirect('dashboard')

        return render(request, self.template_name)



class LogoutUsuarioView(View):
    def get(self, request):
        logout(request)
        return redirect('login')



class  ConfiguraAutorizacaoView(View):
    template_name = 'usuario/cadastrarusuario.html'

    
    def get(self, request):
        return redirect('cadastrar_usuario')

    
    def post(self, request):
        id_usuario = request.POST.get('usuario_adicionar')
        id_permissao = request.POST.get('permissao_adicionar')

        usuario_emissor = request.user.perfil
        usuario_receptor = Perfil.objects.get(id=id_usuario)
        permissao = Permissao.objects.get(id=id_permissao)
        UsuarioPermissao.objects.create(permissao=permissao, perfil_emissor=usuario_emissor, perfil_receptor=usuario_receptor)

        messages.add_message(request, messages.INFO, 'Permissao adiciona ao colaborador.')

        return redirect('cadastrar_usuario')


class UsuarioGerenteView(View):
    def get(self, request, id):
        perfil = Perfil.objects.get(id=id)
        if perfil.gerente:
            perfil.gerente = False
        else:
            perfil.gerente = True
        perfil.save()
        return redirect('administrador_setor')


class UsuarioAdministradorView(View):
    def get(self, request, id):
        user = User.objects.get(id=id)
        if user.is_superuser:
            user.is_superuser = False
        else:
            user.is_superuser = True
        user.save()
        return redirect('administrador_setor')


class UsuarioAtivoView(View):
    def get(self, request, id):
        user = User.objects.get(id=id)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect('administrador_setor')
