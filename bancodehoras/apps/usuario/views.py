from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.base import View

from apps.core.models import *
from apps.core.views.controller import FuncionalidadesCore
from movimentacao.views import seleciona_dados
from apps.usuario.forms import RegistrarUsuarioForm


class LoginUsuarioView(View):
    template_name = 'usuario/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:

            username = request.POST.get('login')
            password = request.POST.get('senha')

            user = authenticate(username=username, password=password)

            if user is None:
                if User.objects.filter(username=username):
                    if User.objects.get(username=username).is_active == False:
                        messages.add_message(request, messages.INFO, 'Usuário inativo.')
                    else:
                        messages.add_message(request, messages.INFO, 'Senha incorreta.')
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
        except:
            messages.add_message(request, messages.INFO, 'Colaborador não cadastrado.')
            return self.get(request)



@login_required(login_url='login')
def cadastrar_usuario(request):
    func = FuncionalidadesCore()
    if not func.superuser(request):
        return redirect('solicitacoes')

    if request.method == 'POST':
        try:
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
                                setor=setor,
                                ch_primeira=dados_form['ch_primeira'],
                                ch_segunda=dados_form['ch_segunda'])
                perfil.save()

                messages.add_message(request, messages.INFO, 'Colaborador cadastrado com sucesso')
                return redirect('administrador_setor_id', id=setor.id)
            else:
                messages.add_message(request, messages.INFO, 'Erro no cadastro, verifique se todos os campos estão preenchidos corretamente.')
                return redirect('setor')
        except Exception:
            messages.add_message(request, messages.INFO, 'Erro no cadastro, verifique se todos os campos estão preenchidos corretamente.')
            return redirect('setor')

    return redirect('setor')


@login_required(login_url='login')
def atualiza_usuario(request, id):
    func = FuncionalidadesCore()
    if not func.superuser(request):
        return redirect('solicitacoes')

    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            matricula = request.POST.get('matricula')
            id_setor = request.POST.get('setor')
            email = request.POST.get('email')
            senha = request.POST.get('senha')
            ch_primeira = request.POST.get('ch_primeira')
            ch_segunda = request.POST.get('ch_segunda')

            if len(nome) == 0 or len(matricula) == 0 or len(id_setor) == 0 or len(email) == 0 or len(ch_primeira) == 0 or len(ch_segunda) == 0:
                messages.add_message(request, messages.INFO, 'Erro na atualização dos dados, com exceção do campo senha, todos os campos devem' +
                                                                'ser preenchidos corretamente')
                return redirect('setor')

            setor = Setor.objects.get(id=id_setor)
            user = User.objects.get(username=id)
            user.username = matricula
            user.email = email
            perfil = user.perfil
            perfil.nome = nome
            perfil.setor = setor
            perfil.ch_primeira = ch_primeira
            perfil.ch_segunda = ch_segunda

            if senha != '':
                user.set_password(senha)
            perfil.save()
            user.save()

            return redirect('usuario_atualiza', id=matricula)
        except:
            messages.add_message(request, messages.INFO, 'Erro na atualização dos dados, verifique se ' +
                                                            'todos os campos estão preenchidos corretamente')
            return redirect('setor')
    else:
        dados = seleciona_dados(request)
        dados['colaborador'] = User.objects.get(username=id)
        dados['setores'] = Setor.objects.all()
        return render(request, 'core/super/mostra-usuario.html', dados)


@login_required(login_url='login')
def logout_usuario(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def usuario_gerente(request, id):
    func = FuncionalidadesCore()
    if not func.superuser(request):
        return redirect('solicitacoes')

    perfil = Perfil.objects.get(id=id)
    if perfil.gerente:
        perfil.gerente = False
    else:
        perfil.gerente = True
    perfil.save()
    return redirect('usuario_atualiza', id=perfil.usuario.username)


@login_required(login_url='login')
def usuario_administrador(request, id):
    func = FuncionalidadesCore()
    if not func.superuser(request):
        return redirect('solicitacoes')

    user = User.objects.get(id=id)
    if user.is_superuser:
        user.is_superuser = False
    else:
        user.is_superuser = True
    user.save()
    return redirect('usuario_atualiza', id=user.username)


@login_required(login_url='login')
def usuario_ativo(request, id):
    func = FuncionalidadesCore()
    if not func.superuser(request):
        return redirect('solicitacoes')

    user = User.objects.get(id=id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect('usuario_atualiza', id=user.username)
