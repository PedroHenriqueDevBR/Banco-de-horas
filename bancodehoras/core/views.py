from django.shortcuts import render, redirect
from django.views.generic.base import View
from core.models import *
from django.contrib import messages


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


class VincularPermissaoView(View):
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