from movimentacao.controller import FuncionalidadesMovimentacao, FormataDados
from core.models import *


class FuncionalidadesCore:

    def formata_dados_do_grafico(self, request):
        funcionalidade = FuncionalidadesMovimentacao([], [])
        autorizado = Status.objects.filter(autorizado=True)[0]
        perfis = request.user.perfil.setor.perfis_do_setor.all()
        resultado = []
    
        for perfil in perfis:
            bancos = perfil.movimentacoes.filter(entrada=True, status=autorizado)
            baixas = perfil.movimentacoes.filter(entrada=False, status=autorizado)
            resultado.append({
                'nome': perfil.nome,
                'total_horas': int(funcionalidade.total_de_horas_disponivel_do_perfil(autorizado, bancos, baixas).split(':')[0])
            })
        
        return resultado
    
    def hash_add(chave, valor):
        if hash_valid(chave, valor):
            return False
        else:
            Hash.objects.create(chave=chave, valor=valor)
            return True

    def hash_get(chave):
        valor = None
        try:
            valor = Hash.objects.filter(chave=chave)[0].valor
        except Exception:
            print('Chave inválida')
        return valor

    def hash_edit(objeto=None, chave=None, valor=None):
        if objeto is not None:
            objeto.valor = valor
            import pdb; pdb.set_trace()
            objeto.save()
            return True
        else:
            if hash_valid(chave, valor):
                try:
                    hash_obj = Hash.objects.filter(chave=chave)[0]
                    hash_obj.valor = valor
                    return True
                except Exception:
                    return False

            return False

    def hash_valid(chave, valor):
        return len(chave) > 0 and len(valor) > 0