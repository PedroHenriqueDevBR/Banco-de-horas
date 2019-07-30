from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from core.models import *
from django.contrib import messages 
from usuario.forms import RegistrarUsuarioForm


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

            if user.is_superuser:
                return redirect('escolha_dashboard')
            elif user.perfil.gerente:
                return redirect('dashboard')
            return redirect('solicitacoes')

        return render(request, self.template_name)


@login_required(login_url='login')
def CadastrarUsuarioView(request):
    if request.method == 'POST':
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
            return redirect('administrador_setor')

    return redirect('administrador_setor')


@login_required(login_url='login')
def AtualizarUsuarioView(request, id):
    if request.method == 'POST':
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


@login_required(login_url='login')
def LogoutUsuarioView(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def UsuarioGerenteView(request, id):
    perfil = Perfil.objects.get(id=id)
    if perfil.gerente:
        perfil.gerente = False
    else:
        perfil.gerente = True
    perfil.save()
    return redirect('administrador_setor')


@login_required(login_url='login')
def UsuarioAdministradorView(request, id):
    user = User.objects.get(id=id)
    if user.is_superuser:
        user.is_superuser = False
    else:
        user.is_superuser = True
    user.save()
    return redirect('administrador_setor')


@login_required(login_url='login')
def UsuarioAtivoView(request, id):
    user = User.objects.get(id=id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect('administrador_setor')
