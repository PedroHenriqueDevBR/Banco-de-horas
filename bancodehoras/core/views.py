from django.shortcuts import render, redirect
from django.views.generic.base import View
from core.models import *
from django.contrib import messages


class SetorView(View):
    template_name = 'usuario/cadastrarusuario.html'

    def get(self, request):
        return render(request, self.template_name)

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